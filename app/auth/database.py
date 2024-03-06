import datetime

from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseOAuthAccountTableUUID
from sqlalchemy import Boolean, DateTime, false, select
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.settings import settings
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


async def delete_expired_guests():
    async with AsyncUOW(AsyncDBSession) as session:
        max_register_date = datetime.datetime.utcnow() - datetime.timedelta(seconds=settings.GUEST_ACCOUNT_LIFETIME)
        query = select(User).where(User.datetime_registered < max_register_date, User.is_guest)
        expired_users = await session.execute(query)
        for user in expired_users.unique().scalars():
            await session.delete(user)


async def delete_expired_unverified_users():
    async with AsyncUOW(AsyncDBSession) as session:
        max_register_date = \
            datetime.datetime.utcnow() - datetime.timedelta(seconds=settings.UNVERIFIED_ACCOUNT_LIFETIME)
        query = select(User).where(User.datetime_registered < max_register_date, User.is_verified == false())
        expired_users = await session.execute(query)
        for user in expired_users.unique().scalars():
            await session.delete(user)
