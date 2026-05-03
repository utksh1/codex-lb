from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from app.core.types import JsonValue


class AnthropicMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str | list[JsonValue]


class AnthropicMessagesRequest(BaseModel):
    model_config = ConfigDict(extra="allow")

    model: str
    messages: list[AnthropicMessage]
    system: str | None = None
    max_tokens: int = 1024
    metadata: JsonValue | None = None
    stop_sequences: list[str] | None = None
    stream: bool = False
    temperature: float | None = None
    top_p: float | None = None
    top_k: int | None = None


class AnthropicMessagesResponse(BaseModel):
    id: str
    type: Literal["message"] = "message"
    role: Literal["assistant"] = "assistant"
    content: list[JsonValue]
    model: str
    stop_reason: str | None = None
    stop_sequence: str | None = None
    usage: JsonValue
