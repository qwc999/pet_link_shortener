from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.user import UserResponse, UserCreate, Token, UserLogin
from app.service.user import UserService
from app.utils.security import create_access_token

auth_router = APIRouter()


@auth_router.post("/register", response_model=UserResponse,
                  summary="Регистрация пользователя")
async def register(
        user_data: UserCreate,
        db: AsyncSession = Depends(get_db)):
    return await UserService(db).register_user(user_data)

@auth_router.post("/login", response_model=Token, summary="Вход в систему")
async def login(
        user_data: UserLogin,
        db: AsyncSession = Depends(get_db)):
    result = await UserService(db).authenticate_user(user_data)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    access_token = create_access_token(data={"sub": result.id})
    return {"access_token": access_token, "token_type": "bearer"}