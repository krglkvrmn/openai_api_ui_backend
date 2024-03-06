from functools import partial

from fastapi.middleware.cors import CORSMiddleware

from app.core.settings import settings

cors_middleware = partial(
    CORSMiddleware,
    allow_origins=[settings.MAIN_PAGE_URL.unicode_string().rstrip('/')],
    allow_methods=['GET', 'POST', 'PUT', 'DELETE'],
    allow_headers=['Authorization', 'X-OPENAI-AUTH-TOKEN'],
    expose_headers=['Location'],
    allow_credentials=True
)
