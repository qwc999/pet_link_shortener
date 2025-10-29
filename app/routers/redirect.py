from fastapi import APIRouter, Request, HTTPException, status
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import RedirectResponse
from app.database import get_db
from app.schemas.link import LinkResponse
from app.service.click import ClickService
from app.service.link import LinkService
from user_agents import parse

redirect_router = APIRouter()


@redirect_router.get("/{short_code}", response_model=LinkResponse,
                     summary = "Перейти по сокращенной ссылке")
async def get_link_for_redirect(
        short_code: str,
        request: Request,
        db: AsyncSession = Depends(get_db)):
    link = await LinkService(db).get_link_for_redirect(short_code)
    if not link:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Link not found or inactive"
        )
    user_agent = parse(request.headers.get("User-Agent"))
    click_data = {
        "ip_address": request.client.host,
        "user_agent": str(user_agent),
        "browser": user_agent.browser.family,
        "os": user_agent.os.family,
        "device_type": "mobile" if user_agent.is_mobile else "desktop"
    }

    await ClickService(db).register_click(link.id, click_data)
    return RedirectResponse(url=link.original_url)
