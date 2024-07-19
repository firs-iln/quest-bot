from contextlib import asynccontextmanager

from sqlalchemy import select, update, func
from sqlalchemy.exc import NoResultFound

from core.interfaces import IUserRepo
from core.schemas import UserSchema, UserCreate
from . import get_session
from .exceptions import NotFoundException, InvalidSchemaError
from .models import User


class UserRepo(IUserRepo):
    def __init__(self, session):
        self.session = session

    async def get(self, telegram_id: int):
        try:
            res = await self.session.execute(select(User).where(User.telegram_id == telegram_id))
            obj = res.scalar_one()
            return UserSchema.model_validate(obj)
        except NoResultFound:
            raise NotFoundException(f"There is no user with id {telegram_id}")

    async def get_all(self, page: int = 0, size: int = 100):
        offset = page * size
        limit = size
        res = await self.session.execute(select(User).offset(offset).limit(limit))
        objects = res.scalars().all()
        return [UserSchema.model_validate(obj) for obj in objects]

    async def create(self, schema: UserCreate):
        if not schema:
            raise InvalidSchemaError("Schema is required")

        instance = User(**schema.model_dump())
        self.session.add(instance)
        await self.session.commit()

        await self.session.refresh(instance)
        return UserSchema.model_validate(instance)

    async def update(self, telegram_id: int, schema: UserCreate):
        if not schema:
            raise InvalidSchemaError("Schema is required")

        clean_kwargs = {key: value for key, value in schema.model_dump().items() if value is not None}
        if not clean_kwargs:
            raise InvalidSchemaError("No valid data to update")

        await self.session.execute(
            update(User).where(User.telegram_id == telegram_id).values(**clean_kwargs))
        await self.session.commit()

        return await self.get(telegram_id)

    async def delete(self, telegram_id: int):
        user = await self.get(telegram_id)
        self.session.delete(user)
        await self.session.commit()
        return user

    async def get_winners_count(self) -> int:
        return (await self.session.execute(select(func.count(User.telegram_id)).where(User.quest_passed))).scalar()

    async def get_winners_position(self, telegram_id: int) -> int:
        res = await self.session.execute(select(User).where(User.quest_passed).order_by(User.quest_passed_at))
        objects = res.scalars().all()
        return [obj.telegram_id for obj in objects].index(telegram_id) + 1


@asynccontextmanager
async def get_user_repo():
    async with get_session() as session:
        yield UserRepo(session)
