import uuid

from fastapi import APIRouter
from starlette import status
from starlette.responses import Response

from app.dependencies.db import AsyncUOWDep
from app.dependencies.users import CurrentActiveUserDep
from app.schemas.app.key import APIKeyCreate, APIKeyRead
from app.services.profile_service import ProfileService

keys_router = APIRouter(prefix="/keys", tags=["keys"])


@keys_router.post('/save')
async def save_api_token(api_token: APIKeyCreate, user: CurrentActiveUserDep, uow: AsyncUOWDep):
    await ProfileService.save_api_token(session=uow, user=user, api_token=api_token)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@keys_router.get('/list', response_model=list[APIKeyRead])
async def get_api_tokens(user: CurrentActiveUserDep, uow: AsyncUOWDep):
    return await ProfileService.get_api_tokens(session=uow, user=user, trim=True)


@keys_router.delete('/delete/{key_id}')
async def delete_api_token(key_id: uuid.UUID, user: CurrentActiveUserDep, uow: AsyncUOWDep):
    await ProfileService.delete_api_token(session=uow, user=user, key_id=key_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
