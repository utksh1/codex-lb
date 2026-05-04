# Tasks: harden-health-ready-timeouts

## 1. Backend

- [x] Add a bounded timeout to `/health/ready` DB checks so the endpoint never blocks for long periods.
- [x] Add/adjust unit coverage for the timeout behavior.

## 2. Verification

- [x] Local: simulate a timeout and confirm `/health/ready` returns `503` quickly.
