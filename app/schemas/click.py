from datetime import datetime

from pydantic import BaseModel


class ClickResponse(BaseModel):
    id: int
    link_id: int
    clicked_at: datetime
    ip_address: str | None
    country: str | None
    browser: str | None
    user_agent: str | None
    device_type: str | None
    os: str | None

    class Config:
        from_attributes = True