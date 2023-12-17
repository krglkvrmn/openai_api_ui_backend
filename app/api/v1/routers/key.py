from fastapi import APIRouter
from starlette import status
from starlette.responses import Response

from app.dependencies.db import AsyncUOWDep
from app.dependencies.users import CurrentActiveUserDep
from app.schemas.app.key import APIKeyCreate
from app.services.profile_service import ProfileService

keys_router = APIRouter(prefix="/keys", tags=["keys"])


@keys_router.post('/save')
async def save_api_token(api_token: APIKeyCreate, user: CurrentActiveUserDep, uow: AsyncUOWDep):
    await ProfileService.save_api_token(session=uow, user=user, api_token=api_token)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@keys_router.delete('/delete')
async def delete_api_token(user: CurrentActiveUserDep, uow: AsyncUOWDep):
    await ProfileService.delete_api_token(session=uow, user=user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
