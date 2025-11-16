from datetime import datetime
from enum import Enum
from sqlalchemy import Boolean, ARRAY
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

from app.database import Base


class PortalRoles(str, Enum):
    PORTAL_ROLE_PAID_USER = "ROLE_PAID_USER"
    PORTAL_ROLE_ADMIN = "ROLE_ADMIN"
    PORTAL_ROLE_SUPERADMIN = "ROLE_SUPERADMIN"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    password = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    roles = Column(ARRAY(String), default=[])

    links = relationship("Link", back_populates="owner")

    @property
    def is_admin(self) -> bool:
        return PortalRoles.PORTAL_ROLE_ADMIN in self.roles

    @property
    def is_superadmin(self) -> bool:
        return PortalRoles.PORTAL_ROLE_SUPERADMIN in self.roles

    def add_role(self, to_add_role: PortalRoles):
        if to_add_role in self.roles:
            self.roles.append(to_add_role)

    def remove_role(self, to_remove_role: PortalRoles):
        return [role for role in self.roles if role != to_remove_role]

