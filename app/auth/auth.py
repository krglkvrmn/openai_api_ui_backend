import uuid

from fastapi import Request
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import AuthenticationBackend, CookieTransport, JWTStrategy

from app.auth.database import User
from app.auth.user_manager import get_user_manager
from app.core.settings import settings
from app.patches.auth import (
    AccessRefreshAuthenticationBackend, AccessRefreshTokensCookieTransport,
    JWTWithRefreshStrategyWriteOnly
)


def get_at_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.ACCESS_TOKEN_SECRET, lifetime_seconds=settings.ACCESS_TOKEN_LIFETIME)


def get_rt_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.REFRESH_TOKEN_SECRET, lifetime_seconds=settings.REFRESH_TOKEN_LIFETIME)


def get_at_rt_jwt_strategy() -> JWTWithRefreshStrategyWriteOnly:
    return JWTWithRefreshStrategyWriteOnly(
        access_token_strategy=get_at_jwt_strategy(),
        refresh_token_strategy=get_rt_jwt_strategy()
    )


access_token_cookie_transport = CookieTransport(
    cookie_name="__at",
    cookie_max_age=settings.ACCESS_TOKEN_COOKIE_LIFETIME,
    cookie_secure=settings.ENV_TYPE == "PROD"
)
refresh_token_cookie_transport = CookieTransport(
    cookie_name="__rt",
    cookie_max_age=settings.REFRESH_TOKEN_COOKIE_LIFETIME,
    cookie_secure=settings.ENV_TYPE == "PROD"
)
access_refresh_token_default_cookie_transport = AccessRefreshTokensCookieTransport(
    access_token_cookie_transport=access_token_cookie_transport,
    refresh_token_cookie_transport=refresh_token_cookie_transport,
)
access_refresh_token_redirect_cookie_transport = AccessRefreshTokensCookieTransport(
    access_token_cookie_transport=access_token_cookie_transport,
    refresh_token_cookie_transport=refresh_token_cookie_transport,
    redirect_url=settings.MAIN_PAGE_URL.unicode_string()
)


at_rt_auth_backend = AccessRefreshAuthenticationBackend(
    name="at-rt-jwt", transport=access_refresh_token_default_cookie_transport, get_strategy=get_at_rt_jwt_strategy
)
at_auth_backend = AuthenticationBackend(
    name="at-jwt",
    transport=access_token_cookie_transport,
    get_strategy=get_at_jwt_strategy,
)
rt_auth_backend = AuthenticationBackend(
    name="rt-jwt",
    transport=refresh_token_cookie_transport,
    get_strategy=get_rt_jwt_strategy,
)
at_rt_auth_oidc_backend = AccessRefreshAuthenticationBackend(
    name="at-rt-jwt-oidc", transport=access_refresh_token_redirect_cookie_transport, get_strategy=get_at_rt_jwt_strategy
)


async def get_enabled_backends(request: Request):
    if request.url.path == "/refresh":
        return [rt_auth_backend]
    return [at_auth_backend]


fastapi_users_at = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [at_auth_backend]
)
fastapi_users_oidc = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [at_rt_auth_oidc_backend]
)
fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [at_auth_backend, rt_auth_backend]
)




