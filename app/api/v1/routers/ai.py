import asyncio
import datetime
import json
import uuid

from fastapi import APIRouter, HTTPException, Request, Response
from starlette import status
from starlette.responses import StreamingResponse

from app.core import crypto
from app.core.settings import settings
from app.db.session import AsyncDBSession
from app.dependencies.db import AsyncUOWDep, RedisDep
from app.dependencies.users import CurrentActiveVerifiedUserDep
from app.schemas.app.chat import ChatRead
from app.schemas.app.sessions import SessionToken
from app.schemas.openai.completions import ChatCompletionsRequest
from app.services.ai_service import AIService
from app.services.stream_analysis import TitleProcessor
from app.services.chat_service import ChatService
from app.services.profile_service import ProfileService
from app.utils.uow import AsyncUOW

ai_router = APIRouter(prefix="/ai", tags=["ai"])

session_token_ttl = datetime.timedelta(seconds=30)


@ai_router.post(
    '/requestStreamingCompletion/chat/{chat_id}',
    status_code=status.HTTP_201_CREATED,
    response_model=SessionToken
)
async def create_completion(
        request: Request,
        response: Response,
        uow: AsyncUOWDep,
        chat_id: int,
        user: CurrentActiveVerifiedUserDep,
        redis: RedisDep,
        request_params: ChatCompletionsRequest,
        debug: bool = False
):
    request_parameters = {"debug": debug, "user_id": str(user.id), 'chat_id': chat_id}
    if not request_params.stream:
        raise HTTPException(
            status_code=422, detail=f"Cannot create a streaming completion with stream={request_params.stream}"
        )

    request_params = AIService.inject_system_prompt(request_params, 'title')

    if not debug:
        request_api_token = request.headers.get('x-openai-auth-token')
        if request_api_token is not None:
            api_token = request_api_token
        else:
            api_tokens = await ProfileService.get_api_tokens(user=user, session=uow, trim=False)
            if not api_tokens:
                raise HTTPException(status_code=400, detail="API key missing")
            api_token = api_tokens[0].key

        request_parameters |= {
            "api_token": crypto.encrypt(api_token).decode(),
            "request_params": request_params.model_dump(mode="json"),
            "endpoint_name": "completions",
        }

    session_token = str(uuid.uuid4())
    request_parameters = json.dumps(request_parameters)
    redis.set(session_token, value=request_parameters, ex=int(session_token_ttl.total_seconds()), nx=True)
    response.headers['Location'] = settings.APP_ORIGIN.unicode_string() + f"api/v1/ai/streamCompletion/{session_token}"
    return {
        "token": session_token,
        "expiry_date": datetime.datetime.utcnow() + session_token_ttl
    }


@ai_router.get('/streamCompletion/{session_token}')
async def stream_completion(session_token: uuid.UUID, redis: RedisDep, user: CurrentActiveVerifiedUserDep):
    request_parameters = redis.get(str(session_token))
    if request_parameters is None:
        raise HTTPException(status_code=410, detail="Session token for receiving a completion expired")

    request_parameters = json.loads(request_parameters)

    if request_parameters.get("user_id") != str(user.id):
        raise HTTPException(status_code=403, detail=f"User {user.id} has no access to this endpoint")
    elif request_parameters.get("debug", True):
        streamer = AIService.debug_streamer()
    else:
        async def update_chat(report: dict):
            async with AsyncDBSession() as session:
                await ChatService.update_chat(
                    session=session, user=user, chat=ChatRead(
                        id=request_parameters['chat_id'],
                        title=report['title'],
                        model=request_parameters['request_params']['model']
                    )
                )
        system_events_processor = TitleProcessor(
            min_length=settings.TITLE_SYS_MESSAGE_MIN_LENGTH,
            max_length=settings.TITLE_SYS_MESSAGE_MAX_LENGTH,
            start_token=settings.TITLE_SYS_MESSAGE_START_TOKEN,
            end_token=settings.TITLE_SYS_MESSAGE_END_TOKEN,
            valid_system_events_action=update_chat
        )
        streamer = AIService.api_proxy_streamer(
            api_token=crypto.decrypt(request_parameters.get("api_token").encode()),
            request_params=ChatCompletionsRequest.model_validate(request_parameters.get("request_params")),
            endpoint_name=request_parameters.get("endpoint_name"),
            system_events_processor=system_events_processor
        )
    return StreamingResponse(streamer, media_type="text/event-stream")
