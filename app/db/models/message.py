import datetime
from dataclasses import dataclass

from sqlalchemy import Integer, Enum, Text, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

import app.schemas.app.message
from app.db.session import Base
from app.schemas import Author
from app.schemas.app import prompt


@dataclass
class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    author: Mapped[Enum] = mapped_column(Enum(Author), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    chat_id: Mapped[int] = mapped_column(Integer, ForeignKey('chats.id'), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), default=datetime.datetime.utcnow)

    chat: Mapped["Chat"] = relationship(back_populates="messages")

    @staticmethod
    def from_pydantic(message: app.schemas.app.message.MessageBase):
        message = message.model_dump()
        return Message(**message)
