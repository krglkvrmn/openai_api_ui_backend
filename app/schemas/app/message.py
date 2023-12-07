import datetime

from pydantic import BaseModel

from app.schemas import Author


class MessageBase(BaseModel):
    author: Author
    content: str
    created_at: datetime.datetime


class MessageCreate(MessageBase):
    chat_id: int


class Message(MessageBase):
    id: int
    chat_id: int

    class Config:
        from_attributes = True
