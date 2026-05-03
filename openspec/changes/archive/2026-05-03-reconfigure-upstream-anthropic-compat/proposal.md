# Proposal: Reconfigure Upstream and Anthropic Compatibility

## Problem
The `codex-lb` proxy needs to support Anthropic's `/v1/messages` API specification (used by tools like Claude Code) while routing to a new OpenAI-compatible upstream (`https://api.utksh.in`).

## Goals
- Update upstream base URL.
- Implement Anthropic request/response models.
- Implement translation layer between Anthropic and OpenAI schemas.
- Support streaming translation for Anthropic clients.
- Handle OpenAI-compatible upstreams in the internal proxy client.

## Solution
1. Update `.env.local`.
2. Add `app/core/anthropic/` for models and translation.
3. Update `app/modules/proxy/api.py` with `/v1/messages` route.
4. Update `app/core/clients/proxy.py` to handle OpenAI-compatible upstream protocols.
