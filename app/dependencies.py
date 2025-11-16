from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_403_FORBIDDEN

from app.config import settings
from app.database import get_db
from app.models import User
from app.models.user import PortalRoles
from app.service.user import UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth")


async def get_current_user(
        db: AsyncSession = Depends(get_db),
        token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = int(payload.get("sub"))
        if not user_id:
            raise credentials_exception
        user = await UserService(db).get_user_by_user_id(user_id)
        if not user:
            raise credentials_exception
        if not user.is_active:
            raise credentials_exception
        return user
    except JWTError:
        raise credentials_exception

def require_role(required_role: PortalRoles):
    async def role_checker(current_user: User = Depends(get_current_user)):
        if required_role not in current_user.roles:
            raise HTTPException(status_code=HTTP_403_FORBIDDEN,
                                 detail=f"Role {required_role} required")
        return current_user
    return role_checker

def require_any_of_roles(required_roles: list[PortalRoles]):
    async def role_checker(current_user: User = Depends(get_current_user)):
        for role in current_user.roles:
            if role in required_roles:
                return current_user
        raise HTTPException(status_code=HTTP_403_FORBIDDEN,
                             detail=f"Required one of these roles: {', '.join(required_roles)}")
    return role_checker

require_admin = require_role(PortalRoles.PORTAL_ROLE_ADMIN)
require_superadmin = require_role(PortalRoles.PORTAL_ROLE_SUPERADMIN)
require_admin_or_superadmin = require_any_of_roles([PortalRoles.PORTAL_ROLE_SUPERADMIN,
                                                    PortalRoles.PORTAL_ROLE_ADMIN])
