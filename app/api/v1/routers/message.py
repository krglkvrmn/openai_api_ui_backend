from fastapi import Depends, APIRouter

from app.auth.schemas import UserRead
from app.dependencies.db import AsyncUOWDep
from app.dependencies.users import CurrentActiveUserDep
from app.schemas.app.message import MessageCreate, Message
from app.services.chat_service import ChatService

message_router = APIRouter(prefix="/messages", tags=["messages"])


@message_router.post('/newMessage', response_model=Message)
async def create_message(message: MessageCreate, user: CurrentActiveUserDep, uow: AsyncUOWDep):
    return await ChatService.add_message(session=uow, user=user, message=message)


@message_router.get('/{message_id}', response_model=Message)
async def get_message(message_id: int, user: CurrentActiveUserDep, uow: AsyncUOWDep):
    return await ChatService.get_message(session=uow, user=user, message_id=message_id)
