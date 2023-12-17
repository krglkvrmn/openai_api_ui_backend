from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.responses import Response

from app.auth.schemas import UserRead
from app.core import crypto
import app.db.models.key as key_models
from app.schemas.app.key import APIKeyCreate, APIKeyRead


class ProfileService:
    @staticmethod
    async def save_api_token(user: UserRead, session: AsyncSession, api_token: APIKeyCreate) -> APIKeyRead:
        query = select(key_models.APIKey).where(key_models.APIKey.user_id == user.id)
        results = await session.execute(query)
        if len(results.scalars().all()) > 0:
            raise HTTPException(status_code=409, detail="User already has an api key configured")

        encrypted_key = crypto.encrypt(api_token.key).decode()
        db_record = key_models.APIKey(key=encrypted_key, user_id=user.id)
        session.add(db_record)
        await session.commit()
        return db_record

    @staticmethod
    async def get_api_token(user: UserRead, session: AsyncSession) -> str:
        query = select(key_models.APIKey.key).where(key_models.APIKey.user_id == user.id)
        results = await session.execute(query)
        encrypted_key = results.scalar_one_or_none()
        if not encrypted_key:
            raise HTTPException(status_code=404, detail="User does not have api keys")
        return crypto.decrypt(encrypted_key)

    @staticmethod
    async def delete_api_token(user: UserRead, session: AsyncSession) -> APIKeyRead:
        query = select(key_models.APIKey).where(key_models.APIKey.user_id == user.id)
        results = await session.execute(query)
        token_data = results.scalar_one_or_none()
        if not token_data:
            raise HTTPException(status_code=404, detail="User does not have api keys")

        await session.delete(token_data)
        return token_data


