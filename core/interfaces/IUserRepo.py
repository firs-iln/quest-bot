from abc import abstractmethod

from core.schemas import UserSchema, UserCreate, UserUpdate


class IUserRepo:
    @abstractmethod
    async def get(self, telegram_id: int) -> UserSchema:
        ...

    async def get_all(self, page: int = 0, size: int = 100) -> list[UserSchema]:
        ...

    @abstractmethod
    async def create(self, schema: UserCreate) -> UserSchema:
        ...

    @abstractmethod
    async def update(self, telegram_id: int, schema: UserUpdate) -> UserSchema:
        ...

    @abstractmethod
    async def delete(self, telegram_id: int) -> None:
        ...

    @abstractmethod
    async def get_winners_count(self) -> int:
        ...

    @abstractmethod
    async def get_winners_position(self, telegram_id: int) -> int:
        ...
