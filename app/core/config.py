import datetime
import os
from pathlib import Path

from dotenv import load_dotenv

from app.utils.io import read_oauth2_config_file

APP_ROOT = Path(__file__).parent.parent
PROJECT_ROOT = APP_ROOT.parent

load_dotenv(APP_ROOT / ".env")

COMPLETIONS_API_DEBUG_RESPONSE = {
    "id": "chatcmpl-123",
    "object": "chat.completion",
    "created": 1677652288,
    "model": "gpt-3.5-turbo-0613",
    "choices": [{
        "index": 0,
        "message": {
            "role": "assistant",
            "content": "\n\nHello there, how may I assist you today?",
        },
        "finish_reason": "stop"
    }],
    "usage": {
        "prompt_tokens": 9,
        "completion_tokens": 12,
        "total_tokens": 21
    }
}
COMPLETIONS_API_STREAM_DEBUG_RESPONSE = [
    {
        "id": "chatcmpl-123",
        "object": "chat.completion.chunk",
        "created": 1677652288,
        "model": "gpt-3.5-turbo",
        "choices": [{
            "index": 0,
            "delta": {
                "role": "assistant",
            },
        }]
    },
    *[{
        "id": "chatcmpl-123",
        "object": "chat.completion.chunk",
        "created": 1677652288,
        "model": "gpt-3.5-turbo",
        "choices": [{
            "index": 0,
            "delta": {
                "content": "Hello ",
            },
        }]
    },
    {
        "id": "chatcmpl-123",
        "object": "chat.completion.chunk",
        "created": 1677652289,
        "model": "gpt-3.5-turbo",
        "choices": [{
            "index": 0,
            "delta": {
                "content": "world ",
            },
        }]
    }] * 20,
    {
        "id": "chatcmpl-123",
        "object": "chat.completion.chunk",
        "created": 1677652289,
        "model": "gpt-3.5-turbo",
        "choices": [{
            "index": 0,
            "delta": {},
            "finish_reason": "stop"
        }]
    }
]


ENV_TYPE = os.environ.get("ENV_TYPE", default="DEV")


APP_LOCAL_HOST = os.getenv("APP_LOCAL_HOST", default='localhost')
APP_LOCAL_PORT = os.getenv("APP_LOCAL_PORT", default=8000)

APP_PUBLIC_HOST = os.getenv("APP_PUBLIC_HOST")


if ENV_TYPE == 'PROD':
    APP_ORIGIN = f'https://{APP_PUBLIC_HOST}'
elif ENV_TYPE == 'DEV':
    APP_ORIGIN = f'http://{APP_LOCAL_HOST}:{APP_LOCAL_PORT}'
else:
    raise ValueError(f'Invalid ENV_TYPE: {ENV_TYPE}')

MAIN_PAGE_URL = APP_ORIGIN if ENV_TYPE == "PROD" else "http://localhost:3001"

# Users
GUEST_ACCOUNT_LIVE_TIME = datetime.timedelta(minutes=10)

# Postgres access
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = Path(os.getenv("POSTGRES_PASSWORD_FILE")).read_text()
POSTGRES_ENGINE = os.getenv("POSTGRES_ENGINE")
DATABASE_URL = f'postgresql+{POSTGRES_ENGINE}://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}'

# Redis
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")

# External APIs
KEY_ENCODE_SECRET_KEY = Path(os.getenv("KEY_ENCODE_SECRET_KEY_FILE")).read_text()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_API_ENDPOINTS = {
    "completions": {"method": "POST", "url": "https://api.openai.com/v1/chat/completions"}
}

OPENAPI_URL = os.getenv('OPENAPI_URL', '/openapi.json')

# Auth tokens
ACCESS_TOKEN_SECRET_KEY = Path(os.getenv("ACCESS_TOKEN_SECRET_KEY_FILE")).read_text()
REFRESH_TOKEN_SECRET_KEY = Path(os.getenv("REFRESH_TOKEN_SECRET_KEY_FILE")).read_text()
VERIFICATION_TOKEN_SECRET_KEY = Path(os.getenv("VERIFICATION_TOKEN_SECRET_KEY_FILE")).read_text()

ACCESS_TOKEN_LIFETIME = int(os.getenv("ACCESS_TOKEN_LIFETIME"))
REFRESH_TOKEN_LIFETIME = int(os.getenv("REFRESH_TOKEN_LIFETIME"))
VERIFICATION_TOKEN_LIFETIME = int(os.getenv("VERIFICATION_TOKEN_LIFETIME"))

ACCESS_TOKEN_COOKIE_LIFETIME = int(os.getenv("ACCESS_TOKEN_COOKIE_LIFETIME"))
REFRESH_TOKEN_COOKIE_LIFETIME = int(os.getenv("REFRESH_TOKEN_COOKIE_LIFETIME"))

# OAuth2 configs
GOOGLE_OAUTH2_CONFIG_FILE = os.getenv("GOOGLE_OAUTH2_CONFIG_FILE")
GITHUB_OAUTH2_CONFIG_FILE = os.getenv("GITHUB_OAUTH2_CONFIG_FILE")
GOOGLE_OAUTH2_CLIENT_ID, GOOGLE_OAUTH2_CLIENT_SECRET = read_oauth2_config_file(GOOGLE_OAUTH2_CONFIG_FILE)
GITHUB_OAUTH2_CLIENT_ID, GITHUB_OAUTH2_CLIENT_SECRET = read_oauth2_config_file(GITHUB_OAUTH2_CONFIG_FILE)

SENDGRID_API_KEY = Path(os.getenv("SENDGRID_API_KEY_FILE")).read_text()
