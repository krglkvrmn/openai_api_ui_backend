import uuid

from pydantic import BaseModel


class SystemPromptCreate(BaseModel):
    content: str


class SystemPromptRead(SystemPromptCreate):
    id: int
    user_id: uuid.UUID
    popularity: int

    class Config:
        from_attributes = True
