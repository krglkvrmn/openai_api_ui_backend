import datetime
import uuid
from typing import Optional

from fastapi_users import schemas
from pydantic import BaseModel, EmailStr


class UserRead(schemas.BaseUser[uuid.UUID]):
    is_guest: bool = False
    datetime_registered: Optional[datetime.datetime] = None


class UserReadShort(BaseModel):
    email: EmailStr
    is_guest: bool = False

    class Config:
        from_attributes = True


class UserCreate(schemas.BaseUserCreate):
    is_guest: bool = False
    datetime_registered: Optional[datetime.datetime] = None


class UserUpdate(schemas.BaseUserUpdate):
    is_guest: bool = False
    datetime_registered: Optional[datetime.datetime] = None
