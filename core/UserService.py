from contextlib import asynccontextmanager
from datetime import datetime

from core.exceptions import UserIsNotWinner
from core.interfaces import IUserRepo
from core.schemas import UserSchema, UserCreate, UserUpdate
from db.UserRepo import get_user_repo


class UserService:
    def __init__(self, user_repo: IUserRepo, winners_amount: int, winners_prizes: dict[int, str]):
        self.user_repo = user_repo
        self.winner_amount = winners_amount
        self.winners_prizes = winners_prizes

    async def get_user(self, telegram_id: int) -> UserSchema:
        return await self.user_repo.get(telegram_id)

    async def create_user(self, user: UserCreate) -> UserSchema:
        return await self.user_repo.create(user)

    async def user_completed_quest(self, telegram_id: int) -> UserSchema:
        update_schema = UserUpdate(quest_passed=True, quest_passed_at=datetime.now())
        return await self.user_repo.update(telegram_id, update_schema)

    async def check_if_user_prizable(self, telegram_id: int) -> bool:
        user = await self.user_repo.get(telegram_id)
        if not user.quest_passed:
            raise UserIsNotWinner()

        winners = await self.user_repo.get_winners_count()
        return winners <= self.winner_amount

    async def get_winners_position(self, telegram_id: int) -> int:
        return await self.user_repo.get_winners_position(telegram_id=telegram_id)

    async def get_winners_prize(self, telegram_id: int) -> str:
        position = await self.user_repo.get_winners_position(telegram_id=telegram_id)
        return self.winners_prizes.get(position)

    async def set_wallet_address(self, telegram_id: int, wallet_address: str) -> UserSchema:
        update_schema = UserUpdate(wallet_address=wallet_address)
        return await self.user_repo.update(telegram_id, update_schema)


@asynccontextmanager
async def get_user_service(winners_amount: int = None, winners_prizes: dict[int, str] = None) -> UserService:
    if not winners_amount:
        winners_amount = 4

    if not winners_prizes:
        winners_prizes = {
            1: '400$',
            2: '300$',
            3: '200$',
            4: '100$',
        }

    async with get_user_repo() as user_repo:
        yield UserService(
            user_repo=user_repo,
            winners_amount=winners_amount,
            winners_prizes=winners_prizes
        )
