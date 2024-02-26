from functools import partial

from fastapi.middleware.cors import CORSMiddleware

from app.core.config import APP_ORIGIN, ENV_TYPE

cors_middleware = partial(
    CORSMiddleware,
    allow_origins=[APP_ORIGIN] if ENV_TYPE == 'PROD' else ['http://localhost:3001'],
    allow_methods=['GET', 'POST', 'PUT', 'DELETE'],
    allow_headers=['Authorization', 'X-OPENAI-AUTH-TOKEN'],
    expose_headers=['Location'],
    allow_credentials=True
)
