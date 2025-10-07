from datetime import datetime

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy.orm import relationship

from app.database import Base


class Click(Base):
    __tablename__ = "clicks"
    id = Column(Integer, primary_key=True)
    link_id = Column(Integer, ForeignKey("links.id"))
    clicked_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    link = relationship("Link", back_populates="clicks")

    # ip_address = Column(String(15))
    # country = Column(String(2))
    # browser = Column(String(15))
