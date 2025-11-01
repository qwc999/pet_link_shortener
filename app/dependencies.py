from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from app.config import settings
from app.database import get_db
from app.models import User
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
        user = await UserService(db).get_user_by_user_id_for_auth(user_id)
        if not user:
            raise credentials_exception
        if not user.is_active:
            raise credentials_exception
        return user
    except JWTError:
        raise credentials_exception
