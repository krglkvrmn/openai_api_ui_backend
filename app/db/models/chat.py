import datetime
import uuid
from dataclasses import dataclass

from sqlalchemy import Integer, String, DateTime, UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

import app.schemas.app.chat
from app.auth.schemas import UserRead
from app.db.session import Base
from app.db.models.message import Message
from app.schemas.app import prompt


@dataclass
class Chat(Base):
    __tablename__ = "chats"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    model: Mapped[str] = mapped_column(String(30), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), default=datetime.datetime.utcnow)
    last_updated: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), default=datetime.datetime.utcnow)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey('user.id'), nullable=False)

    messages: Mapped[list["Message"]] = relationship(
        back_populates="chat", cascade='all, delete-orphan', order_by=Message.created_at
    )
    user: Mapped["User"] = relationship(back_populates="chats")

    @staticmethod
    def from_pydantic(chat: app.schemas.app.chat.ChatBase, user: UserRead):
        chat = chat.model_dump()
        messages = [Message(**message) for message in chat.pop("messages")]
        chat = Chat(**chat, messages=messages, user_id=user.id)
        return chat
