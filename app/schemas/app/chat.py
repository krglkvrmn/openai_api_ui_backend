import datetime
from typing import Optional

from pydantic import BaseModel

from app.schemas.app.message import MessageInNewChatCreate, MessageInfoRead


class ChatBase(BaseModel):
    title: str
    model: str
    created_at: Optional[datetime.datetime] = None
    last_updated: Optional[datetime.datetime] = None


class ChatRead(ChatBase):
    id: int

    class Config:
        from_attributes = True


class ChatInfoRead(ChatRead):
    pass


class ChatFullRead(ChatRead):
    messages: list[MessageInfoRead] = []


class ChatFullCreate(ChatBase):
    messages: list[MessageInNewChatCreate] = []
