from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from app.services.user_service import UserService
from app.db.schemas.user import UserCreate, UserResponse, TokenResponse, LoginRequest
from app.core.dependencies import get_user_service
from datetime import timedelta,datetime
from app.core.config import settings

router = APIRouter()

@router.post("/", response_model=UserResponse)
async def create_user(
    user_create: UserCreate,
    user_service: UserService = Depends(get_user_service)
):
    return await user_service.create_user(user_create)

@router.get("/{user_id}", response_model=UserResponse)
async def read_user(
    user_id: int,
    user_service: UserService = Depends(get_user_service)
):
    user = await user_service.get_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/", response_model=List[UserResponse])
async def list_users(
    user_service: UserService = Depends(get_user_service)
):
    return await user_service.get_all_users()

@router.post("/login", response_model=TokenResponse)
async def login_for_access_token(
    login_request: LoginRequest,
    user_service: UserService = Depends(get_user_service)
):
    user = await user_service.authenticate_user(login_request.username, login_request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    expires_at = datetime.now() + access_token_expires
    access_token = await user_service.create_access_token(user, access_token_expires)
    await user_service.manage_token(user, access_token, expires_at)
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/logout")
async def logout(
    token: str,
    user_service: UserService = Depends(get_user_service)
):
    await user_service.logout_user(token)
    return {"msg": "Successfully logged out"}
