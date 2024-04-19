import asyncio
from functools import partial

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.core.settings import settings

cors_middleware = partial(
    CORSMiddleware,
    allow_origins=[settings.MAIN_PAGE_URL.unicode_string().rstrip('/')],
    allow_methods=['GET', 'POST', 'PUT', 'DELETE'],
    allow_headers=['Authorization', 'X-OPENAI-AUTH-TOKEN'],
    expose_headers=['Location'],
    allow_credentials=True
)


def add_latency_middleware_generator(latency: float):
    async def _latency_middleware(request: Request, call_next) -> Response:
        response = await call_next(request)
        await asyncio.sleep(latency)
        return response
    return _latency_middleware


latency_middleware = add_latency_middleware_generator(latency=settings.RESPONSE_LATENCY)
