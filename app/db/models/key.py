import uuid
from dataclasses import dataclass

from sqlalchemy import UUID, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class APIKey(Base):
    __tablename__ = "api_key"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, nullable=False, default=uuid.uuid4)
    key: Mapped[str] = mapped_column(String, nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey('user.id'), nullable=False)

    user: Mapped["User"] = relationship(back_populates="api_key")
