# Proposal: harden-health-ready-timeouts

## Why

On Render, the service health check probes `GET /health/ready` and expects a quick response.
When the database is slow or the connection pool is saturated, `/health/ready` can block on DB
I/O long enough for Render to report:

- `HTTP health check failed (timed out after 5 seconds)`

That leads to instance flapping even when the service would otherwise recover.

## What Changes

- Add an explicit short timeout around the DB work performed by `GET /health/ready`.
- If the timeout is exceeded, return `503 Service unavailable` quickly instead of hanging.

## Impact

- Render health checks fail fast (503) instead of timing out.
- Operators get clearer failure signals and fewer false-positive restarts.

