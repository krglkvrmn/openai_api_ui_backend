from fastapi import APIRouter

from app.dependencies.db import AsyncUOWDep
from app.dependencies.users import CurrentActiveUserDep, CurrentActiveVerifiedUserDep
from app.schemas.app.prompt import SystemPromptRead
from app.services.chat_service import ChatService

prompt_router = APIRouter(prefix="/prompt", tags=["prompt"])


@prompt_router.get('/system/popular', response_model=list[SystemPromptRead])
async def get_popular_system_prompts(user: CurrentActiveVerifiedUserDep, uow: AsyncUOWDep, limit: int | None = None):
    return await ChatService.get_top_system_prompts(session=uow, user=user, limit=limit)


@prompt_router.delete('/system/deletePrompt/{prompt_id}', response_model=SystemPromptRead)
async def delete_system_prompt(prompt_id: int, user: CurrentActiveVerifiedUserDep, uow: AsyncUOWDep):
    return await ChatService.delete_system_prompt(session=uow, user=user, prompt_id=prompt_id)
