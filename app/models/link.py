from datetime import datetime

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Text
from sqlalchemy.orm import relationship

from app.database import Base


class Link(Base):
    __tablename__ = "links"
    id = Column(Integer, primary_key=True)
    original_url = Column(Text, nullable=False)
    short_code = Column(Text, unique=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="links")
    clicks = relationship("Click", back_populates="link")
