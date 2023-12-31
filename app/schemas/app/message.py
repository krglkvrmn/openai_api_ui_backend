import datetime
from typing import Optional

from pydantic import BaseModel

from app.schemas import Author


class MessageBase(BaseModel):
    author: Author
    content: str
    created_at: Optional[datetime.datetime] = None


class MessageCreate(MessageBase):
    chat_id: int


class Message(MessageBase):
    id: int
    chat_id: int

    class Config:
        from_attributes = True


class MessageOverview(MessageBase):
    id: int
    author: Author
    created_at: Optional[datetime.datetime]

