from fastapi import APIRouter

from app.auth.auth import at_rt_auth_backend, fastapi_users, fastapi_users_at
from app.auth.schemas import UserCreate, UserReadShort, UserUpdate
from app.dependencies.users import CurrentActiveUserDep

auth_router = APIRouter(prefix='')

auth_router.include_router(
    fastapi_users.get_auth_router(at_rt_auth_backend),
    prefix="/auth/jwt",
    tags=["auth"]
)

auth_router.include_router(
    fastapi_users.get_register_router(UserReadShort, UserCreate),
    prefix="/auth",
    tags=["auth"]
)
auth_router.include_router(
    fastapi_users_at.get_users_router(UserReadShort, UserUpdate),
    prefix="/users",
    tags=["users"]
)


@auth_router.post('/refresh')
async def refresh_token(user: CurrentActiveUserDep):
    return await at_rt_auth_backend.login(strategy=at_rt_auth_backend.get_strategy(), user=user)
