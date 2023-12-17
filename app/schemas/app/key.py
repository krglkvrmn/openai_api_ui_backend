import uuid

from pydantic import BaseModel


class APIKeyBase(BaseModel):
    key: str


class APIKeyRead(APIKeyBase):
    id: uuid.UUID
    user_id: uuid.UUID


APIKeyCreate = APIKeyBase
