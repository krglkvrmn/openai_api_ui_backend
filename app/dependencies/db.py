from typing import Annotated

import redis
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import AsyncDBSession
from app.utils.uow import AsyncUOW


async def get_uow() -> AsyncSession:
    async with AsyncUOW(AsyncDBSession) as session:
        yield session


def get_redis() -> redis.Redis:
    r = redis.Redis(host='localhost')
    try:
        yield r
    finally:
        r.close()


AsyncUOWDep = Annotated[AsyncSession, Depends(get_uow)]
RedisDep = Annotated[redis.Redis, Depends(get_redis)]
