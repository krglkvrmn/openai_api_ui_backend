from typing import Annotated

from fastapi import Depends

from app.auth.auth import fastapi_users, get_enabled_backends
from app.auth.database import User

current_active_user = fastapi_users.current_user(active=True, get_enabled_backends=get_enabled_backends)
current_active_superuser = fastapi_users.current_user(
    active=True, superuser=True, get_enabled_backends=get_enabled_backends
)

CurrentActiveUserDep = Annotated[User, Depends(current_active_user)]
CurrentActiveSuperUserDep = Annotated[User, Depends(current_active_superuser)]
