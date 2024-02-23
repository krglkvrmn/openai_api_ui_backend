from sqlalchemy import Select, select
from sqlalchemy.orm import selectinload

from app.auth.schemas import UserRead
from app.db.models.chat import Chat
from app.db.models.message import Message
from app.db.models.prompt import SystemPrompt


class ChatQueriesMixin:
    @staticmethod
    def select_chats() -> Select:
        return select(Chat).options(selectinload(Chat.messages))

    @classmethod
    def select_user_chats(cls, user: UserRead) -> Select:
        return cls.select_chats().where(Chat.user_id == user.id)

    @classmethod
    def select_chat_by_id(cls, chat_id: int) -> Select:
        return cls.select_chats().where(Chat.id == chat_id)

    @classmethod
    def select_user_chat_by_id(cls, chat_id: int, user: UserRead) -> Select:
        return cls.select_chats().where(Chat.id == chat_id, Chat.user_id == user.id)

    @staticmethod
    def select_message_by_id(message_id: int) -> Select:
        return select(Message).where(Message.id == message_id)

    @staticmethod
    def select_user_message_by_id(message_id: int, user: UserRead) -> Select:
        return select(Message) \
            .join(Chat, Message.chat_id == Chat.id) \
            .where(Message.id == message_id, Chat.user_id == user.id)

    @staticmethod
    def select_system_prompt_by_content(content: str) -> Select:
        return select(SystemPrompt).where(SystemPrompt.content == content)
