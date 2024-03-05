from fastapi import APIRouter

from app.dependencies.db import AsyncUOWDep
from app.dependencies.users import CurrentActiveUserDep, CurrentActiveVerifiedUserDep
from app.schemas.app.chat import ChatFullCreate, ChatFullRead, ChatInfoRead, ChatRead
from app.services.chat_service import ChatService

chat_router = APIRouter(prefix="/chats", tags=["chats"])


@chat_router.post('/newChat', response_model=ChatFullRead)
async def create_chat(chat: ChatFullCreate, user: CurrentActiveVerifiedUserDep, uow: AsyncUOWDep):
    return await ChatService.add_chat(chat=chat, user=user, session=uow)


@chat_router.put('/updateChat', response_model=ChatInfoRead)
async def update_chat(chat: ChatRead, user: CurrentActiveVerifiedUserDep, uow: AsyncUOWDep):
    return await ChatService.update_chat(chat=chat, user=user, session=uow)


@chat_router.delete('/deleteChat/{chat_id}', response_model=ChatInfoRead)
async def delete_chat(chat_id: int, user: CurrentActiveVerifiedUserDep, uow: AsyncUOWDep):
    return await ChatService.delete_chat(chat_id=chat_id, user=user, session=uow)


@chat_router.get('/all', response_model=list[ChatInfoRead])
async def get_all_chats(user: CurrentActiveVerifiedUserDep, uow: AsyncUOWDep):
    return await ChatService.get_all_chats(user=user, session=uow)


@chat_router.get('/{chat_id}', response_model=ChatFullRead)
async def get_chat(chat_id: int, user: CurrentActiveVerifiedUserDep, uow: AsyncUOWDep):
    return await ChatService.get_chat(session=uow, user=user, chat_id=chat_id)
