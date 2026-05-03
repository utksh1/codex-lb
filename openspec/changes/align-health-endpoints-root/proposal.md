# Proposal: align-health-endpoints-root

## Why

Production deployments (Render/Railway/Kubernetes) probe liveness/readiness via root health endpoints such as:

- `GET /health/live`
- `GET /health/ready`

In this repo, the health router was mounted under the dashboard `/api` prefix (`/api/health/*`), which caused:

- Infra health checks configured for `/health/ready` to fail against some environments.
- Swagger/OpenAPI to disagree between local vs production.
- The frontend "Upstream status" widget to rely on a non-standard `/api/health/upstream` path.

## What Changes

- Expose health endpoints at the root (`/health/*`) instead of under `/api/*`.
- Update the dashboard frontend to call `GET /health/upstream`.
- Update Netlify redirects so the `codex.utksh.in` frontend forwards `/health/*` to the backend service.

## Impact

- Infra probes work consistently across local + production.
- Swagger/OpenAPI documents the correct health endpoints.
- `/api/health/*` is no longer available (it returns 404).

