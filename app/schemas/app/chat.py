import datetime

from pydantic import BaseModel

from app.schemas.app.message import MessageBase, Message, MessageCreate


class ChatBase(BaseModel):
    title: str
    model: str
    created_at: datetime.datetime
    last_updated: datetime.datetime


class ChatCreate(ChatBase):
    messages: list[MessageBase] = []


class ChatRead(ChatBase):
    id: int
    messages: list[Message | MessageCreate] = []

    class Config:
        from_attributes = True


class ChatOverview(ChatBase):
    id: int


class SingleChatResponse(ChatBase):
    messages: list[Message | MessageCreate]
