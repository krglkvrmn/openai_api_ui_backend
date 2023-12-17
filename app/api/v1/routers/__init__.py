from fastapi import APIRouter

from app.api.v1.routers.ai import ai_router
from app.api.v1.routers.chat import chat_router
from app.api.v1.routers.key import keys_router
from app.api.v1.routers.message import message_router
from app.api.v1.routers.prompt import prompt_router

v1_router = APIRouter(prefix="/v1")
v1_router.include_router(ai_router)
v1_router.include_router(chat_router)
v1_router.include_router(message_router)
v1_router.include_router(prompt_router)
v1_router.include_router(keys_router)

