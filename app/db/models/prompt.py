import uuid

from sqlalchemy import ForeignKey, Integer, Text, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.auth.schemas import UserRead
from app.db.session import Base
from app.schemas.app.prompt import SystemPromptCreate


class SystemPrompt(Base):
    __tablename__ = "system_prompt"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    content: Mapped[str] = mapped_column(Text)
    popularity: Mapped[int] = mapped_column(Integer)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey('user.id', ondelete='CASCADE'), nullable=False)

    user: Mapped["User"] = relationship(back_populates='prompts')

    @staticmethod
    def from_pydantic(prompt: SystemPromptCreate, user: UserRead = None) -> "SystemPrompt":
        prompt = prompt.model_dump(mode='python')
        user_id = user.id if user else None
        return SystemPrompt(**prompt, user_id=user_id)
