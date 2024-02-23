import uuid

from sqlalchemy import ForeignKey, String, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.auth.schemas import UserRead
from app.db.session import Base
from app.schemas.app.key import APIKeyBase


class APIKey(Base):
    __tablename__ = "api_key"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, nullable=False, default=uuid.uuid4)
    key: Mapped[str] = mapped_column(String, nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey('user.id'), nullable=False)

    user: Mapped["User"] = relationship(back_populates="api_key")

    @staticmethod
    def from_pydantic(api_key: APIKeyBase, user: UserRead) -> "APIKey":
        api_key = api_key.model_dump(mode='python')
        user_id = user.id if user else None
        return APIKey(**api_key, user_id=user_id)
