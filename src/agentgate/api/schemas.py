from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class Message(BaseModel):
    model_config = ConfigDict(extra="allow")
    role: Literal["system", "user", "assistant", "tool"]
    content: str


class ChatRequest(BaseModel):
    messages: list[Message] = Field(..., min_length=1)
    model: str = Field(...)
    temperature: float | None = Field(default=1, ge=0, le=2)
    max_tokens: int | None = Field(default=None, gt=0)


class Usage(BaseModel):
    prompt_tokens: int = Field(..., ge=0)
    completion_tokens: int = Field(..., ge=0)
    total_tokens: int = Field(..., ge=0)


class Choice(BaseModel):
    index: int = Field(..., ge=0)
    message: Message
    finish_reason: str | None = None


class ChatResponse(BaseModel):
    id: str
    object: Literal["chat.completion"] = "chat.completion"
    created: int = Field(..., ge=0)
    model: str
    choices: list[Choice]
    usage: Usage
