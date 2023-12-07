from functools import partial

from fastapi.middleware.cors import CORSMiddleware


cors_middleware = partial(
    CORSMiddleware,
    allow_origins=['http://localhost:3001'],
    allow_methods=['*'],
    allow_headers=['*'],
    allow_credentials=True
)