from datetime import datetime
from pydantic import BaseModel, field_validator, HttpUrl
import validators


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
    # mode=before позволяет выполнить валидацию и только потом переделать в объект HttpUrl
    @field_validator("original_url", mode="before")
    @classmethod
    def pre_validate_url(cls, v: str) -> str:
        if isinstance(v, str):
            v = v.strip()
            if not v.startswith(("https://", "http://")):
                v = "https://" + v
            if not validators.url(v):
                raise ValueError("Invalid URL format")
        return v
