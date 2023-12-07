import asyncio
import json

import httpx

from app.core.config import OPENAI_API_ENDPOINTS, OPENAI_API_KEY, COMPLETIONS_API_DEBUG_RESPONSE, \
    COMPLETIONS_API_STREAM_DEBUG_RESPONSE
from app.schemas.openai.completions import ChatCompletionsRequest, ChatCompletionsResponseChunk


class AIService:
    @staticmethod
    async def debug_streamer():
        for chunk_data in COMPLETIONS_API_STREAM_DEBUG_RESPONSE:
            await asyncio.sleep(0.3)
            json_chunk_data = json.dumps(chunk_data)
            chunk = f'data: {json_chunk_data}\n\n'
            yield chunk.encode('utf-8')
        yield 'data: [DONE]'

    @classmethod
    async def api_proxy_streamer(cls, request_params: ChatCompletionsRequest, endpoint_name: str):
        headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}
        params = request_params.model_dump(mode="json", exclude_none=True)
        async with httpx.AsyncClient() as client:
            async with client.stream(
                    **OPENAI_API_ENDPOINTS[endpoint_name], json=params, headers=headers) as response:
                async for event in response.aiter_lines():
                    yield event
