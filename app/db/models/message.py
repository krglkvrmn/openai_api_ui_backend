import datetime
from dataclasses import dataclass

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base
from app.schemas import Author
from app.schemas.app.message import MessageBase


@dataclass
class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    author: Mapped[Enum] = mapped_column(Enum(Author), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    chat_id: Mapped[int] = mapped_column(Integer, ForeignKey('chats.id', ondelete='CASCADE'), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), default=datetime.datetime.utcnow)

    chat: Mapped["Chat"] = relationship(back_populates="messages")

    @staticmethod
    def from_pydantic(message: MessageBase) -> "Message":
        message = message.model_dump(mode='python')
        return Message(**message)
