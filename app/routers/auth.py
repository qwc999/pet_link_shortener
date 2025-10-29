from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
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


@auth_router.post("/auth", response_model=Token, summary="Вход в систему")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user_data = UserLogin(email=form_data.username, password=form_data.password)
    user = await UserService(db).authenticate_user(user_data)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token = create_access_token(
        data={"sub": str(user.id)}
    )
    return {"access_token": access_token, "token_type": "bearer"}