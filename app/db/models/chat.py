import datetime
import uuid

from sqlalchemy import DateTime, ForeignKey, Integer, String, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.auth.schemas import UserRead
from app.db.models.message import Message
from app.db.session import Base
from app.schemas.app.chat import ChatBase


class Chat(Base):
    __tablename__ = "chats"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    model: Mapped[str] = mapped_column(String(30), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), default=datetime.datetime.utcnow)
    last_updated: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), default=datetime.datetime.utcnow)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey('user.id', ondelete='CASCADE'), nullable=False)

    messages: Mapped[list["Message"]] = relationship(
        back_populates="chat", cascade='all, delete-orphan', order_by=Message.created_at
    )
    user: Mapped["User"] = relationship(back_populates="chats")

    @staticmethod
    def from_pydantic(chat: ChatBase, user: UserRead = None) -> "Chat":
        chat = chat.model_dump(mode='python')
        orm_messages = [Message(**message) for message in chat.pop("messages", [])]
        user_id = user.id if user is not None else None
        orm_chat = Chat(**chat, messages=orm_messages, user_id=user_id)
        return orm_chat
