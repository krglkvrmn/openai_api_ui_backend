import datetime
import uuid
from typing import Any, Optional

from fastapi_users import schemas
from pydantic import BaseModel, EmailStr, PositiveInt, model_validator

from app.core.settings import settings


class UserRead(schemas.BaseUser[uuid.UUID]):
    is_guest: bool = False
    datetime_registered: Optional[datetime.datetime] = None


class UserReadShort(BaseModel):
    email: EmailStr
    is_guest: bool = False
    is_verified: bool = False
    datetime_registered: Optional[datetime.datetime]
    lifetime: Optional[PositiveInt] = None

    @model_validator(mode='after')
    def check_account_lifetime(self) -> 'UserReadShort':
        self.lifetime = settings.GUEST_ACCOUNT_LIFETIME if self.is_guest else None
        return self

    class Config:
        from_attributes = True


class UserCreate(schemas.BaseUserCreate):
    is_guest: bool = False
    datetime_registered: Optional[datetime.datetime] = None


class UserUpdate(schemas.BaseUserUpdate):
    is_guest: bool = False
    datetime_registered: Optional[datetime.datetime] = None
