import datetime
from typing import Optional

from pydantic import BaseModel

from app.schemas import Author


class MessageBase(BaseModel):
    author: Author
    created_at: Optional[datetime.datetime] = None


class MessageRead(MessageBase):
    id: int
    chat_id: int

    class Config:
        from_attributes = True


class MessageFullRead(MessageRead):
    content: str


class MessageInfoRead(MessageRead):
    pass


class MessageInNewChatCreate(MessageBase):
    content: str


class MessageAddToChatCreate(MessageInNewChatCreate):
    chat_id: int


