# Tasks: Reconfigure Upstream and Anthropic Compatibility

- [x] Update `CODEX_LB_UPSTREAM_BASE_URL` in `.env.local`
- [x] Create Anthropic models in `app/core/anthropic/models.py`
- [x] Implement translation logic in `app/core/anthropic/translation.py`
- [x] Implement SSE stream translation
- [x] Add `/v1/messages` endpoint to `app/modules/proxy/api.py`
- [x] Update `ProxyService` in `app/core/clients/proxy.py` to support OpenAI upstreams
- [x] Implement request/response translation for OpenAI upstreams
- [x] Verify with unit tests (scratch scripts)
