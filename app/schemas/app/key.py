import uuid

from pydantic import BaseModel


class APIKeyBase(BaseModel):
    key: str


class APIKeyReadShort(APIKeyBase):
    id: uuid.UUID

    class Config:
        from_attributes = True


class APIKeyRead(APIKeyReadShort):
    user_id: uuid.UUID

    class Config:
        from_attributes = True


APIKeyCreate = APIKeyBase
