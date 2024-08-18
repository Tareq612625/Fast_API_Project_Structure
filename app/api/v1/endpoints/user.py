from typing import List
from fastapi import APIRouter, Depends, HTTPException
from app.services.user_service import UserService
from app.db.schemas.user import UserCreate, UserResponse
from app.core.dependencies import get_async_session, get_user_service

router = APIRouter()

@router.post("/", response_model=UserResponse)
async def create_user(user_create: UserCreate, user_service: UserService = Depends(get_user_service)):
    return await user_service.create_user(user_create)

@router.get("/{user_id}", response_model=UserResponse)
async def read_user(user_id: int, user_service: UserService = Depends(get_user_service)):
    user = await user_service.get_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/", response_model=List[UserResponse])
async def list_users(user_service: UserService = Depends(get_user_service)):
    return await user_service.get_all_users()
