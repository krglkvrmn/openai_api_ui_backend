import datetime

from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseOAuthAccountTableUUID
from sqlalchemy import Boolean, DateTime, select
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.config import GUEST_ACCOUNT_LIVE_TIME
from app.db.session import AsyncDBSession, Base
from app.dependencies.db import AsyncUOWDep
from app.patches.auth import SQLAlchemyCustomUserDatabase
from app.utils.uow import AsyncUOW


class OAuthAccount(SQLAlchemyBaseOAuthAccountTableUUID, Base):
    pass


class User(SQLAlchemyBaseUserTableUUID, Base):
    is_guest: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    datetime_registered: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=False),
        default=lambda: datetime.datetime.utcnow(),
        nullable=False
    )
    api_key: Mapped["APIKey"] = relationship(back_populates="user", cascade='all, delete-orphan')
    chats: Mapped[list["Chat"]] = relationship(back_populates="user", cascade='all, delete-orphan')
    prompts: Mapped[list["SystemPrompt"]] = relationship(back_populates="user", cascade='all, delete-orphan')

    oauth_accounts: Mapped[list[OAuthAccount]] = relationship("OAuthAccount", lazy="joined")


async def get_user_db(session: AsyncUOWDep):
    yield SQLAlchemyCustomUserDatabase(session, User, OAuthAccount)


async def delete_expired_users():
    async with AsyncUOW(AsyncDBSession) as session:
        max_register_date = datetime.datetime.utcnow() - GUEST_ACCOUNT_LIVE_TIME
        query = select(User).where(User.datetime_registered < max_register_date, User.is_guest)
        expired_users = await session.execute(query)
        for user in expired_users:
            await session.delete(user)
