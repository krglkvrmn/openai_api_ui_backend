import asyncio
import datetime
import json
import uuid

from fastapi import APIRouter, Request, HTTPException, Response
from starlette import status
from starlette.responses import StreamingResponse

from app.core import crypto
from app.dependencies.db import AsyncUOWDep, RedisDep
from app.dependencies.users import CurrentActiveUserDep
from app.schemas.app.sessions import SessionToken
from app.schemas.openai.completions import ChatCompletionsResponse, ChatCompletionsResponseChunk, ChatCompletionsRequest
from app.services.ai_service import AIService
from app.services.profile_service import ProfileService

ai_router = APIRouter(prefix="/ai", tags=["ai"])

session_token_ttl = datetime.timedelta(seconds=30)


@ai_router.post(
    '/requestStreamingCompletion',
    status_code=status.HTTP_201_CREATED,
    response_model=SessionToken
)
async def create_completion(
        request: Request,
        response: Response,
        uow: AsyncUOWDep,
        user: CurrentActiveUserDep,
        redis: RedisDep,
        request_params: ChatCompletionsRequest,
        debug: bool = False
):
    request_parameters = {"debug": debug, "user_id": str(user.id)}
    if not request_params.stream:
        raise HTTPException(
            status_code=422, detail=f"Cannot create a streaming completion with stream={request_params.stream}"
        )

    if not debug:
        request_api_token = request.headers.get('x-openai-auth-token')
        if request_api_token is not None:
            api_token = request_api_token
        else:
            api_tokens = await ProfileService.get_api_tokens(user=user, session=uow, trim=False)
            api_token = api_tokens[0].key

        request_parameters |= {
            "api_token": crypto.encrypt(api_token).decode(),
            "request_params": request_params.model_dump(mode="json"),
            "endpoint_name": "completions",
        }

    session_token = str(uuid.uuid4())
    request_parameters = json.dumps(request_parameters)
    redis.set(session_token, value=request_parameters, ex=int(session_token_ttl.total_seconds()), nx=True)
    response.headers['Location'] = f"http://localhost:8000/api/v1/ai/streamCompletion/{session_token}"
    return {
        "token": session_token,
        "expiry_date": datetime.datetime.utcnow() + session_token_ttl
    }


@ai_router.get('/streamCompletion/{session_token}')
def stream_completion(session_token: uuid.UUID, redis: RedisDep, user: CurrentActiveUserDep):
    request_parameters = redis.get(str(session_token))
    if request_parameters is None:
        raise HTTPException(status_code=410, detail="Session token for receiving a completion expired")

    request_parameters = json.loads(request_parameters)

    if request_parameters.get("user_id") != str(user.id):
        raise HTTPException(status_code=403, detail=f"User {user.id} has no access to this endpoint")
    elif request_parameters.get("debug", True):
        streamer = AIService.debug_streamer()
    else:
        streamer = AIService.api_proxy_streamer(
            api_token=crypto.decrypt(request_parameters.get("api_token").encode()),
            request_params=ChatCompletionsRequest.model_validate(request_parameters.get("request_params")),
            endpoint_name=request_parameters.get("endpoint_name")
        )
    return StreamingResponse(streamer, media_type="text/event-stream")
