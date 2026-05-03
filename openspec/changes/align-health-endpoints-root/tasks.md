# Tasks: align-health-endpoints-root

## 1. Backend routes

- [x] Mount health router at root (`/health/*`) instead of `/api/health/*`.
- [x] Confirm OpenAPI lists `/health/*` paths and `/api/health/*` is absent.

## 2. Frontend

- [x] Update upstream status widget to fetch `GET /health/upstream`.

## 3. Netlify routing

- [x] Add Netlify redirect for `/health/*` → backend `/health/:splat` to keep `codex.utksh.in` working.

## 4. Verification

- [x] Local: `GET /health/ready` returns 200.
- [x] Local: dashboard routes still return 200 via the frontend proxy.

