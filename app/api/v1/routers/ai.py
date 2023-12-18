import asyncio
import json

from fastapi import APIRouter, Request
from starlette.responses import StreamingResponse

from app.dependencies.db import AsyncUOWDep
from app.dependencies.users import CurrentActiveUserDep
from app.schemas.openai.completions import ChatCompletionsResponse, ChatCompletionsResponseChunk, ChatCompletionsRequest
from app.services.ai_service import AIService
from app.services.profile_service import ProfileService

ai_router = APIRouter(prefix="/ai", tags=["ai"])


@ai_router.post('/createCompletion')
async def create_completion(
        request: Request,
        uow: AsyncUOWDep,
        user: CurrentActiveUserDep,
        request_params: ChatCompletionsRequest,
        debug: bool = False
):
    if request_params.stream and not debug:
        request_api_token = request.headers.get('x-openai-auth-token')
        if request_api_token is not None:
            api_token = request_api_token
        else:
            api_tokens = await ProfileService.get_api_tokens(user=user, session=uow, trim=False)
            api_token = api_tokens[0].key
        streamer = AIService.api_proxy_streamer(
            api_token=api_token,
            request_params=request_params,
            endpoint_name='completions'
        )
        return StreamingResponse(streamer)
    elif request_params.stream and debug:
        streamer = AIService.debug_streamer()
        return StreamingResponse(streamer)
