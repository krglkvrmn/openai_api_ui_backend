from fastapi import APIRouter

from app.auth.auth import get_user_manager, fastapi_users_at, fastapi_users, at_auth_backend, at_rt_auth_backend
from app.auth.schemas import UserRead, UserCreate, UserUpdate, UserReadShort
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
