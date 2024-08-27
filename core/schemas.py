from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class UserCreate(BaseModel):
    telegram_id: int
    username: Optional[str]


class UserUpdate(BaseModel):
    username: Optional[str] = None
    quest_passed: Optional[bool] = None
    quest_passed_at: Optional[datetime] = None
    wallet_address: Optional[str] = None
    story_link: Optional[str] = None
    passed_first_day: Optional[bool] = None
    passed_second_day: Optional[bool] = None


class UserSchema(BaseModel):
    telegram_id: int
    username: Optional[str]
    quest_passed: bool
    quest_passed_at: Optional[datetime]
    wallet_address: Optional[str]
    story_link: Optional[str]
    passed_first_day: Optional[bool]
    passed_second_day: Optional[bool]

    model_config = ConfigDict(from_attributes=True)
