from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.click import ClickResponse
from app.schemas.link import LinkResponse, LinkCreate
from app.service.click import ClickService
from app.service.link import LinkService


link_router = APIRouter(prefix="/links")


@link_router.get("/my", response_model=list[LinkResponse], summary="Получить все ссылки пользователя")
async def get_my_links(
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)):
    return await LinkService(db).get_user_links(current_user.id)

@link_router.post("/", response_model=LinkResponse, summary="Создать ссылку")
async def create_link(
        link_data: LinkCreate,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)):
    try:
        return await LinkService(db).create_link(link_data, current_user.id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@link_router.delete("/", response_model=LinkResponse, summary="Деактивировать ссылку")
async def delete_link(
        link_id: int,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)):
    result = await LinkService(db).delete_link(link_id, current_user.id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail="Link not found")
    return result

@link_router.get("/{link_id}", response_model=LinkResponse, summary="Получить ссылку по id")
async def get_link_by_id(
        link_id: int,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)):
    result = await LinkService(db).get_link_by_id(link_id, current_user.id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail="Link not found")
    return result

@link_router.get("/{link_id}/clicks", response_model=list[ClickResponse],
                 summary="Получить список переходов по ссылке")
async def get_clicks_by_link_id(
        link_id: int,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)):
    result = await ClickService(db).get_clicks_by_link_id(link_id, current_user.id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail="Link not found")
    return result
