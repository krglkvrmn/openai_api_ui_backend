from typing import Optional

from pydantic import BaseModel, Json

from app.schemas import Author


class ChatCompletionsFunctionCall(BaseModel):
    name: str
    arguments: str


class ChatCompletionFunction(BaseModel):
    name: str
    parameters: dict
    description: Optional[str] = None


class ChatCompletionsDelta(BaseModel):
    role: Optional[Author] = None
    content: Optional[str] = None
    function_call: Optional[ChatCompletionsFunctionCall] = None


class ChatCompletionsMessage(ChatCompletionsDelta):
    name: Optional[str] = None


class ChatCompletionsUsage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class ChatCompletionsChoiceBase(BaseModel):
    index: int
    finish_reason: Optional[str] = None


class ChatCompletionsChoice(ChatCompletionsChoiceBase):
    message: ChatCompletionsMessage


class ChatCompletionsChoiceChunk(ChatCompletionsChoiceBase):
    delta: ChatCompletionsDelta


class ChatCompletionsRequest(BaseModel):
    model: str
    messages: list[ChatCompletionsMessage]
    functions: Optional[list[ChatCompletionFunction]] = None
    function_call: Optional[ChatCompletionsFunctionCall] = None
    temperature: Optional[float] = None
    top_p: Optional[float] = None
    n: Optional[int] = None
    stream: Optional[bool] = None
    stop: Optional[str | list[str]] = None
    max_tokens: Optional[int] = None
    presence_penalty: Optional[float] = None
    frequency_penalty: Optional[float] = None
    logit_bias: Optional[Json] = None
    user: Optional[str] = None


class ChatCompletionsResponseBase(BaseModel):
    id: str
    object: str
    created: int
    model: str


class ChatCompletionsResponseChunk(ChatCompletionsResponseBase):
    choices: list[ChatCompletionsChoiceChunk]


class ChatCompletionsResponse(ChatCompletionsResponseBase):
    choices: list[ChatCompletionsChoice]
    usage: ChatCompletionsUsage

    class Config:
        from_attributes = True


