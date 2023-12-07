import uuid

from sqlalchemy import Integer, Text, UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base
from app.schemas.app import prompt


class SystemPrompt(Base):
    __tablename__ = "system_prompt"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    content: Mapped[str] = mapped_column(Text)
    popularity: Mapped[int] = mapped_column(Integer)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey('user.id'), nullable=False)

    user: Mapped["User"] = relationship(back_populates='prompts')

    @staticmethod
    def from_pydantic(prompt: prompt.SystemPromptCreate):
        prompt = prompt.model_dump()
        return SystemPrompt(**prompt)
