# app/services/user_service.py
from typing import List
from app.db.models.user import User
from app.db.repositories.user_repository import UserRepository
from app.db.schemas.user import UserCreate, UserUpdate

class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def create_user(self, user_create: UserCreate) -> User:
        user = User(username=user_create.username, email=user_create.email, full_name=user_create.full_name)
        return await self.repository.create(user)

    async def get_user(self, user_id: int) -> User:
        return await self.repository.get(user_id)

    async def get_all_users(self) -> List[User]:
        return await self.repository.get_all()
