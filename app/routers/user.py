from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.dependencies import get_current_user
from app.models import User
from app.schemas.user import UserResponse, UserUpdate
from app.service.user import UserService

user_router = APIRouter()

# todo : запретить удаленным пользователям действия

@user_router.get("/me", response_model=UserResponse, summary="Получение своего профиля")
async def get_me(
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)):
    user = await UserService(db).get_user_by_user_id_for_auth(current_user.id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found or inactive")
    return user

@user_router.delete("/me", response_model=UserResponse, summary="Деактивировать пользователя")
async def deactivate_me(
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)):
    user = await UserService(db).deactivate_user(current_user.id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found or inactive")
    return user

@user_router.patch("/me", response_model=UserResponse, summary="Обновить пользователя")
async def update_me(
        data: UserUpdate,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)):
    try:
        user = await UserService(db).update_user(current_user.id, data)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found or inactive")
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e))