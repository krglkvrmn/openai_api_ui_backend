import asyncio
import json

import httpx

from app.services.debug_data.ai_service_debug_data import COMPLETIONS_API_STREAM_DEBUG_RESPONSE
from app.core.settings import settings
from app.schemas.openai.completions import ChatCompletionsRequest


class AIService:
    @staticmethod
    async def debug_streamer():
        for chunk_data in COMPLETIONS_API_STREAM_DEBUG_RESPONSE:
            await asyncio.sleep(0.01)
            json_chunk_data = json.dumps(chunk_data)
            chunk = f'data: {json_chunk_data}\n\n'
            yield chunk.encode('utf-8')
        yield 'data: [DONE]'

    @classmethod
    async def api_proxy_streamer(cls, api_token: str, request_params: ChatCompletionsRequest, endpoint_name: str):
        headers = {"Authorization": f"Bearer {api_token}"}
        params = request_params.model_dump(mode="json", exclude_none=True)
        async with httpx.AsyncClient() as client:
            async with client.stream(
                    **settings.OPENAI_API_ENDPOINTS[endpoint_name], json=params, headers=headers) as response:
                if response.status_code == 401:
                    response_content = json.loads(await response.aread())
                    yield f'data: {json.dumps(response_content)}\n\n'
                async for event in response.aiter_lines():
                    yield event
