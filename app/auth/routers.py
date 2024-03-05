from fastapi import APIRouter

from app.auth.auth import (
    at_rt_auth_backend, at_rt_auth_oidc_backend, fastapi_users, fastapi_users_at
)
from app.auth.oauth2_clients import github_oauth_client, google_oauth_client
from app.auth.schemas import UserCreate, UserReadShort, UserUpdate
from app.core.config import APP_ORIGIN, GITHUB_OAUTH2_CLIENT_SECRET, GOOGLE_OAUTH2_CLIENT_SECRET
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
    fastapi_users.get_oauth_router(
        google_oauth_client,
        at_rt_auth_oidc_backend,
        GOOGLE_OAUTH2_CLIENT_SECRET,
        redirect_url=APP_ORIGIN + '/auth/google/callback',
        associate_by_email=True,
        is_verified_by_default=True
    ),
    prefix="/auth/google",
    tags=["auth"]
)
auth_router.include_router(
    fastapi_users.get_oauth_router(
        github_oauth_client,
        at_rt_auth_oidc_backend,
        GITHUB_OAUTH2_CLIENT_SECRET,
        redirect_url=APP_ORIGIN + '/auth/github/callback',
        associate_by_email=True,
        is_verified_by_default=True
    ),
    prefix="/auth/github",
    tags=["auth"]
)
auth_router.include_router(
    fastapi_users_at.get_users_router(UserReadShort, UserUpdate),
    prefix="/users",
    tags=["users"]
)
auth_router.include_router(
    fastapi_users.get_verify_router(UserReadShort),
    prefix='/auth',
    tags=['auth']
)


@auth_router.post('/refresh')
async def refresh_token(user: CurrentActiveUserDep):
    return await at_rt_auth_backend.login(strategy=at_rt_auth_backend.get_strategy(), user=user)
