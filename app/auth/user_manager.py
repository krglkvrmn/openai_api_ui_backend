import uuid
from typing import Optional
from urllib.parse import urlencode

from fastapi import BackgroundTasks, Depends
from fastapi_users import BaseUserManager, UUIDIDMixin
from sendgrid import Mail, SendGridAPIClient
from starlette.requests import Request

from app.auth.database import User, get_user_db
from app.core.settings import settings
from app.services.email_service import send_forgot_password_email, send_verification_email


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = settings.RESET_PASSWORD_TOKEN_SECRET
    verification_token_secret = settings.VERIFICATION_TOKEN_SECRET.get_secret_value()
    verification_token_lifetime_seconds = settings.VERIFICATION_TOKEN_LIFETIME

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        send_forgot_password_email(token=token, email=user.email)

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        send_verification_email(token=token, email=user.email)


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
