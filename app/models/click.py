from datetime import datetime

from sqlalchemy import String, Text
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy.orm import relationship

from app.database import Base


class Click(Base):
    __tablename__ = "clicks"
    id = Column(Integer, primary_key=True, index=True)
    link_id = Column(Integer, ForeignKey("links.id"))
    clicked_at = Column(DateTime, default=datetime.utcnow)

    ip_address = Column(String(15))
    country = Column(String(2))
    browser = Column(String(15))
    user_agent = Column(Text)
    device_type = Column(String(20))
    os = Column(String(15))

    link = relationship("Link", back_populates="clicks")
