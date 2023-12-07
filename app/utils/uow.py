from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession


class AsyncUOW:
    def __init__(self, session_maker: async_sessionmaker[AsyncSession]):
        self.session_maker = session_maker
        self.session: AsyncSession | None = None

    async def __aenter__(self):
        self.session = self.session_maker()
        return self.session

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            await self.session.commit()
        else:
            await self.session.rollback()
        await self.session.close()
        self.session = None
