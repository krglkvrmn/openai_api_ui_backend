from functools import partial

from fastapi.middleware.cors import CORSMiddleware

from app.core.config import APP_ORIGIN, ENV_TYPE, MAIN_PAGE_URL

cors_middleware = partial(
    CORSMiddleware,
    allow_origins=[MAIN_PAGE_URL],
    allow_methods=['GET', 'POST', 'PUT', 'DELETE'],
    allow_headers=['Authorization', 'X-OPENAI-AUTH-TOKEN'],
    expose_headers=['Location'],
    allow_credentials=True
)
