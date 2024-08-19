from typing import List, Optional
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import HTTPException, status
from passlib.context import CryptContext
from app.db.models.user import User
from app.db.models.jwt_token import Token
from app.db.repositories.user_repository import UserRepository
from app.db.schemas.user import UserCreate
from app.core.config import settings

class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    async def create_user(self, user_create: UserCreate) -> User:
        hashed_password = self.pwd_context.hash(user_create.password)
        user = User(username=user_create.username, email=user_create.email, full_name=user_create.full_name, password=hashed_password)
        return await self.repository.create(user)

    async def get_user(self, user_id: int) -> Optional[User]:
        return await self.repository.get(user_id)

    async def get_all_users(self) -> List[User]:
        return await self.repository.get_all()

    async def authenticate_user(self, username: str, password: str) -> Optional[User]:
        user = await self.repository.get_by_username(username)
        if user is None or not self.pwd_context.verify(password, user.password):
            return None
        return user

    async def create_access_token(self, user: User, expires_delta: timedelta) -> str:
        to_encode = {"sub": str(user.id), "exp": datetime.now() + expires_delta}
        return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    async def manage_token(self, user: User, token: str, access_token_expires:datetime):
        existing_token = await self.repository.get_token_by_user_id(user.id)
        if existing_token:
            existing_token.token = token
            existing_token.is_active = True
            existing_token.expires_at = access_token_expires
            await self.repository.update_token(existing_token)
        else:
            new_token = Token(user_id=user.id, token=token,expires_at=access_token_expires)
            await self.repository.create_token(new_token)

    async def logout_user(self, token: str):
        await self.repository.deactivate_token(token)
