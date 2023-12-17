import datetime
import os
from pathlib import Path

from dotenv import load_dotenv


APP_ROOT = Path(__file__).parent.parent

load_dotenv(APP_ROOT / ".env")
load_dotenv(APP_ROOT / ".secret" / "access_token_secret_key.env")
load_dotenv(APP_ROOT / ".secret" / "refresh_token_secret_key.env")
load_dotenv(APP_ROOT / ".secret" / "key_encode_secret_key.env")

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

# Users
GUEST_ACCOUNT_LIVE_TIME = datetime.timedelta(minutes=1)


# Postgres access
PG_DB = os.getenv("PG_DB")
PG_HOST = os.getenv("PG_HOST")
PG_USER = os.getenv("PG_USER")
PG_PASSWORD = os.getenv("PG_PASSWORD")
PG_ENGINE = os.getenv("PG_ENGINE")
SQL_DATABASE_URL = f'postgresql+{PG_ENGINE}://{PG_USER}:{PG_PASSWORD}@{PG_HOST}/{PG_DB}'

# External APIs
KEY_ENCODE_SECRET_KEY = os.getenv("KEY_ENCODE_SECRET_KEY")
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_API_ENDPOINTS = {
    "completions": {"method": "POST", "url": "https://api.openai.com/v1/chat/completions"}
}

# Auth tokens
ACCESS_TOKEN_SECRET_KEY = os.getenv("ACCESS_TOKEN_SECRET_KEY")
REFRESH_TOKEN_SECRET_KEY = os.getenv("REFRESH_TOKEN_SECRET_KEY")

ACCESS_TOKEN_LIFETIME = int(os.getenv("ACCESS_TOKEN_LIFETIME"))
REFRESH_TOKEN_LIFETIME = int(os.getenv("REFRESH_TOKEN_LIFETIME"))

ACCESS_TOKEN_COOKIE_LIFETIME = int(os.getenv("ACCESS_TOKEN_COOKIE_LIFETIME"))
REFRESH_TOKEN_COOKIE_LIFETIME = int(os.getenv("REFRESH_TOKEN_COOKIE_LIFETIME"))
