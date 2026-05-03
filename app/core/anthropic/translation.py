from __future__ import annotations

from collections.abc import AsyncIterator

from app.core.anthropic.models import AnthropicMessagesRequest, AnthropicMessagesResponse
from app.core.openai.chat_requests import ChatCompletionsRequest
from app.core.openai.chat_responses import ChatCompletion, ChatCompletionChunk
from app.core.types import JsonValue
from app.core.utils.sse import format_sse_data, parse_sse_data_json


def anthropic_to_openai_request(request: AnthropicMessagesRequest) -> ChatCompletionsRequest:
    messages: list[JsonValue] = []
    
    # System message
    if request.system:
        messages.append({"role": "system", "content": request.system})
    
    # Conversation messages
    for msg in request.messages:
        messages.append({
            "role": msg.role,
            "content": msg.content
        })
    
    openai_payload: dict[str, JsonValue] = {
        "model": request.model,
        "messages": messages,
        "max_tokens": request.max_tokens,
        "stream": request.stream,
    }
    
    if request.temperature is not None:
        openai_payload["temperature"] = request.temperature
    if request.top_p is not None:
        openai_payload["top_p"] = request.top_p
    if request.stop_sequences:
        openai_payload["stop"] = request.stop_sequences
        
    return ChatCompletionsRequest.model_validate(openai_payload)


def openai_to_anthropic_response(completion: ChatCompletion) -> AnthropicMessagesResponse:
    content: list[JsonValue] = []
    for choice in completion.choices:
        if choice.message.content:
            content.append({
                "type": "text",
                "text": choice.message.content
            })
            
    usage: dict[str, int] = {}
    if completion.usage:
        usage["input_tokens"] = completion.usage.prompt_tokens or 0
        usage["output_tokens"] = completion.usage.completion_tokens or 0

    return AnthropicMessagesResponse(
        id=completion.id,
        content=content,
        model=completion.model,
        usage=usage,
        stop_reason=completion.choices[0].finish_reason if completion.choices else None
    )


async def stream_openai_to_anthropic(stream: AsyncIterator[str]) -> AsyncIterator[str]:
    # This is a simplified version of Anthropic streaming events
    # Anthropic uses a more complex event structure
    # For now, let's just yield content_block_delta for text
    
    yield "event: message_start\n"
    yield f"data: {format_sse_data({'type': 'message_start', 'message': {'id': 'msg_temp', 'type': 'message', 'role': 'assistant', 'content': [], 'model': 'temp', 'usage': {'input_tokens': 0, 'output_tokens': 0}}})}\n\n"
    
    yield "event: content_block_start\n"
    yield f"data: {format_sse_data({'type': 'content_block_start', 'index': 0, 'content_block': {'type': 'text', 'text': ''}})}\n\n"
    
    async for line in stream:
        payload = parse_sse_data_json(line)
        if not payload:
            continue
        
        # Check for DONE
        if line.strip() == "data: [DONE]":
            break
            
        try:
            chunk = ChatCompletionChunk.model_validate(payload)
            for choice in chunk.choices:
                if choice.delta.content:
                    yield "event: content_block_delta\n"
                    yield f"data: {format_sse_data({'type': 'content_block_delta', 'index': 0, 'delta': {'type': 'text_delta', 'text': choice.delta.content}})}\n\n"
        except Exception:
            # Skip invalid chunks
            continue
            
    yield "event: content_block_stop\n"
    yield f"data: {format_sse_data({'type': 'content_block_stop', 'index': 0})}\n\n"
    
    yield "event: message_delta\n"
    yield f"data: {format_sse_data({'type': 'message_delta', 'delta': {'stop_reason': 'end_turn', 'stop_sequence': None}, 'usage': {'output_tokens': 0}})}\n\n"
    
    yield "event: message_stop\n"
    yield f"data: {format_sse_data({'type': 'message_stop'})}\n\n"
