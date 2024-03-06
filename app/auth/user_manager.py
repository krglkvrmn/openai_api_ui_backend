import uuid
from typing import Optional
from urllib.parse import urlencode

from fastapi import Depends
from fastapi_users import BaseUserManager, UUIDIDMixin
from sendgrid import Mail, SendGridAPIClient
from starlette.requests import Request

from app.auth.database import User, get_user_db
from app.core.settings import settings


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    # reset_password_token_secret = ACCESS_TOKEN_SECRET_KEY
    verification_token_secret = settings.VERIFICATION_TOKEN_SECRET
    verification_token_lifetime_seconds = settings.VERIFICATION_TOKEN_LIFETIME

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")
        verifiication_link = settings.MAIN_PAGE_URL.unicode_string() + 'verification?' + urlencode({'vt': token})
        print(verifiication_link)
        # message = Mail(
        #     from_email='verification@chat.krglkvrmn.me',
        #     to_emails=user.email,
        #     subject='Verify Your Email Address',
        #     html_content=f'Please verify your email by following this link: <a href={verifiication_link}>Verify</b>'
        # )
        # sg = SendGridAPIClient(SENDGRID_API_KEY)
        # sg.send(message)


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
