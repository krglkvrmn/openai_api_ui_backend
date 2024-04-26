import datetime
from collections.abc import Sequence

from fastapi import HTTPException
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.schemas import UserRead
from app.db.models import prompt as prompt_models
from app.db.models.chat import Chat
from app.db.models.message import Message
from app.db.models.prompt import SystemPrompt
from app.schemas import Author
from app.schemas.app.chat import ChatBase, ChatFullCreate, ChatRead
from app.schemas.app.message import MessageAddToChatCreate
from app.services.common_queries import ChatQueriesMixin


class ChatService(ChatQueriesMixin):
    @classmethod
    async def get_message(cls, session: AsyncSession, user: UserRead, message_id: int) -> Message:
        query = cls.select_user_message_by_id(message_id=message_id, user=user)
        result = await session.execute(query)
        message = result.scalar_one_or_none()
        if message is None:
            raise HTTPException(status_code=404, detail='Message not found')
        return message

    @classmethod
    async def add_message(cls, session: AsyncSession, user: UserRead, message: MessageAddToChatCreate) -> Message:
        query = cls.select_user_chat_by_id(chat_id=message.chat_id, user=user)
        result = await session.execute(query)
        if result.one_or_none() is None:
            raise HTTPException(status_code=404, detail='Chat not found')
        message = Message.from_pydantic(message)
        session.add(message)
        await session.commit()
        await session.refresh(message)
        return message

    @classmethod
    async def get_chat(cls, session: AsyncSession, user: UserRead, chat_id: int) -> Chat:
        query = cls.select_user_chat_by_id(chat_id=chat_id, user=user)
        result = await session.execute(query)
        chat = result.scalar_one_or_none()
        if chat is None:
            raise HTTPException(status_code=404, detail='Chat not found')
        return chat

    @classmethod
    async def get_all_chats(cls, user: UserRead, session: AsyncSession) -> Sequence[Chat]:
        query = cls.select_user_chats(user=user).order_by(desc('last_updated'))
        result = await session.execute(query)
        chats = result.scalars().all()
        return chats

    @classmethod
    async def add_chat(cls, session: AsyncSession, user: UserRead, chat: ChatFullCreate) -> Chat:
        if len(chat.messages) > 0 and (first_message := chat.messages[0]).author == Author.system:
            await cls._add_update_system_prompt(session=session, user=user, prompt_content=first_message.content)
        chat = Chat.from_pydantic(chat=chat, user=user)
        session.add(chat)
        await session.commit()
        await session.refresh(chat, ["messages"])
        return chat

    @classmethod
    async def _add_update_system_prompt(cls, session: AsyncSession, user: UserRead, prompt_content: str) -> None:
        query = cls.select_system_prompt_by_content(content=prompt_content)
        result = await session.execute(query)
        prompt = result.scalar_one_or_none()
        if prompt is not None:
            prompt.popularity += 1
        else:
            prompt = prompt_models.SystemPrompt(content=prompt_content, popularity=1, user_id=user.id)
            session.add(prompt)

    @staticmethod
    async def get_top_system_prompts(
            session: AsyncSession, user: UserRead, limit: int | None
    ) -> Sequence[SystemPrompt]:
        query = select(SystemPrompt).where(SystemPrompt.user_id == user.id).order_by(desc('popularity')).limit(limit)
        result = await session.execute(query)
        return result.scalars().all()

    @staticmethod
    async def delete_system_prompt(session: AsyncSession, user: UserRead, prompt_id: int) -> SystemPrompt:
        query = select(SystemPrompt).where(SystemPrompt.id == prompt_id, SystemPrompt.user_id == user.id)
        result = await session.execute(query)
        db_prompt = result.scalar_one_or_none()
        if not db_prompt:
            raise HTTPException(status_code=404, detail='Prompt not found')

        await session.delete(db_prompt)
        await session.commit()
        return db_prompt

    @classmethod
    async def update_chat(cls, session: AsyncSession, user: UserRead, chat: ChatRead) -> Chat:
        query = cls.select_user_chat_by_id(chat_id=chat.id, user=user)
        result = await session.execute(query)
        db_chat = result.scalar_one_or_none()
        if not db_chat:
            raise HTTPException(status_code=404, detail="Chat not found")

        db_chat.title = chat.title
        db_chat.model = chat.model
        db_chat.last_updated = chat.last_updated or datetime.datetime.utcnow()

        await session.commit()
        await session.refresh(db_chat)
        return db_chat

    @classmethod
    async def delete_chat(cls, session: AsyncSession, user: UserRead, chat_id: int) -> Chat:
        query = cls.select_user_chat_by_id(chat_id=chat_id, user=user)
        result = await session.execute(query)
        db_chat = result.scalar_one_or_none()
        if not db_chat:
            raise HTTPException(status_code=404, detail="Chat not found")

        await session.delete(db_chat)
        await session.commit()
        return db_chat
