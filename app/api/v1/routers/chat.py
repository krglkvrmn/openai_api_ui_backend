from fastapi import Depends, APIRouter

from app.auth.auth import fastapi_users
from app.auth.database import User
from app.dependencies.db import AsyncUOWDep
from app.dependencies.users import CurrentActiveUserDep, CurrentActiveSuperUserDep
from app.schemas.app.chat import ChatCreate, ChatRead, ChatOverview
from app.services.chat_service import ChatService

chat_router = APIRouter(prefix="/chats", tags=["chats"])


@chat_router.post('/newChat', response_model=ChatRead)
async def create_chat(chat: ChatCreate, user: CurrentActiveUserDep, uow: AsyncUOWDep):
    return await ChatService.add_chat(chat=chat, user=user, session=uow)


@chat_router.put('/updateChat', response_model=ChatRead)
async def update_chat(chat: ChatRead, user: CurrentActiveUserDep, uow: AsyncUOWDep):
    return await ChatService.update_chat(chat=chat, user=user, session=uow)


@chat_router.delete('/deleteChat/{chat_id}', response_model=ChatOverview)
async def delete_chat(chat_id: int, user: CurrentActiveUserDep, uow: AsyncUOWDep):
    return await ChatService.delete_chat(chat_id=chat_id, user=user, session=uow)


@chat_router.get('/all', response_model=list[ChatOverview])
async def get_all_chats(user: CurrentActiveUserDep, uow: AsyncUOWDep):
    return await ChatService.get_all_chats(user=user, session=uow)


@chat_router.get('/{chat_id}', response_model=ChatRead)
async def get_chat(chat_id: int, user: CurrentActiveUserDep, uow: AsyncUOWDep):
    return await ChatService.get_chat(session=uow, user=user, chat_id=chat_id)
