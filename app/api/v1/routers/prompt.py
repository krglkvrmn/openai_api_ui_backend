from fastapi import APIRouter

from app.dependencies.db import AsyncUOWDep
from app.dependencies.users import CurrentActiveUserDep
from app.schemas.app.prompt import SystemPrompt, SystemPromptResponse
from app.services.chat_service import ChatService

prompt_router = APIRouter(prefix="/prompt", tags=["prompt"])


@prompt_router.get('/system/popular', response_model=list[SystemPromptResponse])
async def get_popular_system_prompts(user: CurrentActiveUserDep, uow: AsyncUOWDep, limit: int | None = None):
    return await ChatService.get_top_system_prompts(session=uow, user=user, limit=limit)


@prompt_router.delete('/system/deletePrompt/{prompt_id}', response_model=SystemPrompt)
async def delete_system_prompt(prompt_id: int, user: CurrentActiveUserDep, uow: AsyncUOWDep):
    return await ChatService.delete_system_prompt(session=uow, prompt_id=prompt_id)
