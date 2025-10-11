from datetime import datetime
from pydantic import BaseModel, HttpUrl


class LinkResponse(BaseModel):
    id: int
    original_url: str
    short_code: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class LinkDelete(BaseModel):
    id: int

class LinkCreate(BaseModel):
    original_url: HttpUrl
