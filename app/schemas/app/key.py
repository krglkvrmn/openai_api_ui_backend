import uuid

from pydantic import BaseModel


class APIKeyBase(BaseModel):
    key: str


class APIKeyRead(APIKeyBase):
    id: uuid.UUID

    class Config:
        from_attributes = True


class APIKeyWithUserRead(APIKeyRead):
    user_id: uuid.UUID


class APIKeyCreate(APIKeyBase):
    pass
