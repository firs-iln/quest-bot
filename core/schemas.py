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


class UserSchema(BaseModel):
    telegram_id: int
    username: Optional[str]
    quest_passed: bool
    quest_passed_at: Optional[datetime]
    wallet_address: Optional[str]

    model_config = ConfigDict(from_attributes=True)
