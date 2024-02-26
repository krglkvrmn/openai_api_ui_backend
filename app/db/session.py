from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

from app.core.config import DATABASE_URL


engine = create_async_engine(DATABASE_URL, echo=False)
AsyncDBSession = async_sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)

Base = declarative_base()


def get_base():
    import app.auth
    import app.db.models
    return Base
