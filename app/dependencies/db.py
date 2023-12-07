from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import AsyncDBSession
from app.utils.uow import AsyncUOW


async def get_uow():
    async with AsyncUOW(AsyncDBSession) as session:
        yield session


AsyncUOWDep = Annotated[AsyncSession, Depends(get_uow)]
