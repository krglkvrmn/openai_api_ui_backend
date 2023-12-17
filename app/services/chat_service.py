import datetime

from fastapi import HTTPException, Depends
from sqlalchemy import desc, select, Select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.orm import Session, selectinload, joinedload, aliased, contains_eager

from app.auth.schemas import UserRead
from app.db.models import message as message_models, chat as chat_models, prompt as prompt_models
from app.schemas import Author
from app.schemas.app.chat import ChatCreate, ChatRead, ChatOverview
from app.schemas.app.message import MessageCreate, Message


class ChatService:
    @staticmethod
    def select_chats_query() -> Select:
        return select(chat_models.Chat).options(selectinload(chat_models.Chat.messages))

    @classmethod
    def select_user_chats_query(cls, user: UserRead) -> Select:
        return cls.select_chats_query().where(chat_models.Chat.user_id == user.id)

    @classmethod
    def select_chat_by_id_query(cls, chat_id: int) -> Select:
        return cls.select_chats_query().where(chat_models.Chat.id == chat_id)

    @classmethod
    def select_user_chat_by_id_query(cls, chat_id: int, user: UserRead) -> Select:
        return cls.select_chats_query().where(
            chat_models.Chat.id == chat_id, chat_models.Chat.user_id == user.id
        )

    @staticmethod
    def select_message_by_id_query(message_id: int) -> Select:
        return select(message_models.Message).where(message_models.Message.id == message_id)

    @staticmethod
    def select_user_message_by_id_query(message_id: int, user: UserRead) -> Select:
        return select(message_models.Message) \
                .join(chat_models.Chat, message_models.Message.chat_id == chat_models.Chat.id) \
                .where(message_models.Message.id == message_id, chat_models.Chat.user_id == user.id)

    @staticmethod
    def select_system_prompt_by_content_query(content: str) -> Select:
        return select(prompt_models.SystemPrompt).where(prompt_models.SystemPrompt.content == content)

    @classmethod
    async def add_message(cls, session: AsyncSession, user: UserRead, message: MessageCreate):
        user_check_query = cls.select_user_chat_by_id_query(message.chat_id, user=user)
        user_check_result = await session.execute(user_check_query)
        if not user_check_result.one_or_none():
            raise HTTPException(status_code=404, detail='Chat not found')
        message = message_models.Message.from_pydantic(message)
        session.add(message)
        await session.commit()
        await session.refresh(message)
        return message

    @classmethod
    async def add_update_system_prompt(cls, session: AsyncSession, user: UserRead, prompt_content: str):
        query = cls.select_system_prompt_by_content_query(prompt_content)
        result = await session.execute(query)
        db_prompt = result.scalar_one_or_none()
        if db_prompt:
            db_prompt.popularity += 1
        else:
            prompt = prompt_models.SystemPrompt(id=None, content=prompt_content, popularity=1, user_id=user.id)
            session.add(prompt)

    @staticmethod
    async def get_top_system_prompts(session: AsyncSession, user: UserRead, limit: int | None):
        query = select(prompt_models.SystemPrompt) \
                    .where(prompt_models.SystemPrompt.user_id == user.id) \
                    .order_by(desc('popularity')).limit(limit)
        result = await session.execute(query)
        return result.scalars().all()

    @staticmethod
    async def delete_system_prompt(session: AsyncSession, prompt_id: int):
        query = select(prompt_models.SystemPrompt).where(prompt_models.SystemPrompt.id == prompt_id)
        result = await session.execute(query)
        db_prompt = result.scalar_one_or_none()
        if not db_prompt:
            raise HTTPException(status_code=404, detail='Prompt not found')

        await session.delete(db_prompt)
        return db_prompt

    @classmethod
    async def add_chat(cls, session: AsyncSession, user: UserRead, chat: ChatCreate):
        first_message = chat.messages[0]
        if first_message.author == Author.system:
            await cls.add_update_system_prompt(session=session, user=user, prompt_content=first_message.content)
        chat = chat_models.Chat.from_pydantic(chat, user)
        session.add(chat)
        await session.commit()
        await session.refresh(chat, ["messages"])
        return chat

    @classmethod
    async def update_chat(cls, session: AsyncSession, user: UserRead, chat: ChatOverview):
        query = cls.select_user_chat_by_id_query(chat.id, user=user)
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
    async def delete_chat(cls, session: AsyncSession, user: UserRead, chat_id: int):
        query = cls.select_user_chat_by_id_query(chat_id, user=user)
        result = await session.execute(query)
        db_chat = result.scalar_one_or_none()
        if not db_chat:
            raise HTTPException(status_code=404, detail="Chat not found")

        await session.delete(db_chat)
        return db_chat

    @classmethod
    async def get_message(cls, session: AsyncSession, user: UserRead, message_id: int):
        query = cls.select_user_message_by_id_query(message_id, user=user)
        result = await session.execute(query)
        message = result.scalar_one_or_none()
        if not message:
            raise HTTPException(status_code=404, detail="Message not found")
        return message

    @classmethod
    async def get_chat(cls, session: AsyncSession, user: UserRead, chat_id: int):
        query = cls.select_user_chat_by_id_query(chat_id, user=user)
        result = await session.execute(query)
        return result.scalar_one()

    @classmethod
    async def get_all_chats(cls, user: UserRead, session: AsyncSession):
        query = cls.select_user_chats_query(user).order_by(desc('last_updated'))
        result = await session.execute(query)
        values = result.scalars().all()
        return values

