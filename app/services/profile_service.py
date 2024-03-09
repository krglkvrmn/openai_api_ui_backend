import math
import uuid

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

import app.db.models.key as key_models
from app.auth.schemas import UserRead
from app.core import crypto
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
    async def get_api_tokens(user: UserRead, session: AsyncSession, trim: bool = True) -> list[APIKeyRead]:
        query = select(key_models.APIKey).where(key_models.APIKey.user_id == user.id)
        results = await session.execute(query)
        tokens_data = [APIKeyRead.model_validate(res) for res in results.scalars().all()]

        for idx, token_data in enumerate(tokens_data):
            decrypted_key = crypto.decrypt(token_data.key)
            key_trim_length = math.ceil(len(decrypted_key) * 0.2)
            key = f'*****{decrypted_key[-key_trim_length:]}' if trim else decrypted_key
            tokens_data[idx].key = key
        return tokens_data

    @staticmethod
    async def delete_api_token(user: UserRead, session: AsyncSession, key_id: uuid.UUID) -> APIKeyRead:
        query = select(key_models.APIKey).where(
            key_models.APIKey.user_id == user.id, key_models.APIKey.id == key_id)
        results = await session.execute(query)
        token_data = results.scalar_one_or_none()
        if not token_data:
            raise HTTPException(status_code=404, detail="User does not have api keys")

        await session.delete(token_data)
        await session.commit()
        return token_data


