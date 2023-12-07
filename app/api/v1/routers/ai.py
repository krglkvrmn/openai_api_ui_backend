import asyncio
import json

from fastapi import APIRouter, Request
from starlette.responses import StreamingResponse

from app.schemas.openai.completions import ChatCompletionsResponse, ChatCompletionsResponseChunk, ChatCompletionsRequest
from app.services.ai_service import AIService

ai_router = APIRouter(prefix="/ai", tags=["ai"])


@ai_router.post('/createCompletion')
async def create_completion(request_params: ChatCompletionsRequest, debug: bool = False):
    if request_params.stream and not debug:
        streamer = AIService.api_proxy_streamer(request_params=request_params, endpoint_name='completions')
        return StreamingResponse(streamer)
    elif request_params.stream and debug:
        streamer = AIService.debug_streamer()
        return StreamingResponse(streamer)
