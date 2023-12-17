import datetime
from typing import Optional

from pydantic import BaseModel

from app.schemas.app.message import MessageBase, Message, MessageCreate, MessageOverview


class ChatBase(BaseModel):
    title: str
    model: str
    created_at: Optional[datetime.datetime] = None
    last_updated: Optional[datetime.datetime] = None


class ChatCreate(ChatBase):
    messages: list[MessageBase] = []


class ChatRead(ChatBase):
    id: int
    messages: list[Message | MessageCreate] = []

    class Config:
        from_attributes = True


class ChatOverview(ChatBase):
    id: int


class ChatWithMessageOverview(ChatOverview):
    messages: list[MessageOverview]