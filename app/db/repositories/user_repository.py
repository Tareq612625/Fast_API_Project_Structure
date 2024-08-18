# app/db/repositories/user_repository.py
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models.user import User

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user: User) -> User:
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def get(self, user_id: int) -> Optional[User]:
        result = await self.session.execute(select(User).filter_by(id=user_id))
        return result.scalars().first()

    async def get_all(self) -> List[User]:
        result = await self.session.execute(select(User))
        return result.scalars().all()
