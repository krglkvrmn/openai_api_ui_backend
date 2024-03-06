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
