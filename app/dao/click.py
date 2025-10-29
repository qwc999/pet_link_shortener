from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Click


class ClickDAO:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_click(self, data: dict) -> Click:
        click = Click(**data)
        self.db.add(click)
        await self.db.commit()
        await self.db.refresh(click)
        return click

    async def get_clicks_by_link_id(self, link_id: int):
        clicks = await self.db.execute(Select(Click).where(Click.link_id == link_id))
        return clicks.scalars().all()