# Tasks: fix-asyncpg-prepared-statement-cache

## 1. Backend

- [x] Disable asyncpg prepared statement caching by default for `postgresql+asyncpg://` URLs.

## 2. Tests

- [x] Add unit coverage for `_postgres_async_connect_args`.

## 3. Verification

- [x] Render deploy succeeds on `codex-lb-backend` and the service starts cleanly.
