import datetime
from dataclasses import dataclass

from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from sqlalchemy import Boolean, DateTime, select, String
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import Mapped, relationship, mapped_column

from app.auth.schemas import UserRead
from app.core.config import GUEST_ACCOUNT_LIVE_TIME
from app.db.session import Base, AsyncDBSession
from app.dependencies.db import AsyncUOWDep
from app.utils.uow import AsyncUOW


@dataclass
class User(SQLAlchemyBaseUserTableUUID, Base):
    is_guest: Mapped[bool] = mapped_column(Boolean, default=False)
    datetime_registered: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=False),
        default=lambda: datetime.datetime.utcnow(),
        nullable=False
    )
    api_key: Mapped["APIKey"] = relationship(back_populates="user", cascade='all, delete-orphan')
    chats: Mapped[list["Chat"]] = relationship(back_populates="user", cascade='all, delete-orphan')
    prompts: Mapped[list["SystemPrompt"]] = relationship(back_populates="user", cascade='all, delete-orphan')


async def get_user_db(session: AsyncUOWDep):
    yield SQLAlchemyUserDatabase(session, User)


async def delete_expired_users():
    async with AsyncUOW(AsyncDBSession) as session:
        max_register_date = datetime.datetime.utcnow() - GUEST_ACCOUNT_LIVE_TIME
        query = select(User).where(User.datetime_registered < max_register_date, User.is_guest)
        expired_users = await session.execute(query)
        for user in expired_users.scalars():
            await session.delete(user)
