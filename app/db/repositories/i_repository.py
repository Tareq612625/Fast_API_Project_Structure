# Repository interfaces (abstract base classes)
from typing import List, TypeVar, Generic
from app.db.models.base import Base

T = TypeVar('T', bound=Base)

class IRepository(Generic[T]):
    async def get(self, id: int) -> T:
        raise NotImplementedError
    
    async def create(self, obj: T) -> T:
        raise NotImplementedError
    
    async def get_all(self) -> List[T]:
        raise NotImplementedError
