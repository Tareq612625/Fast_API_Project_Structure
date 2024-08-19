from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models.user import User
from app.db.models.jwt_token import Token

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

    async def get_by_username(self, username: str) -> Optional[User]:
        result = await self.session.execute(select(User).filter_by(username=username))
        return result.scalars().first()

    async def create_token(self, token: Token):
        self.session.add(token)
        await self.session.commit()

    async def update_token(self, token: Token):
        self.session.add(token)
        await self.session.commit()

    async def get_token_by_user_id(self, user_id: int) -> Optional[Token]:
        result = await self.session.execute(select(Token).filter_by(user_id=user_id))
        return result.scalars().first()

    async def deactivate_token(self, token_str: str):
        result = await self.session.execute(select(Token).filter_by(token=token_str))
        token = result.scalars().first()
        if token:
            token.is_active = False
            self.session.add(token)
            await self.session.commit()
