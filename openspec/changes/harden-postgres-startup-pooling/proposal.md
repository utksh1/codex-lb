## Why
Render deployments against the linked Supabase project are failing during startup migration because the application and migration paths consume too many PostgreSQL session-pooler slots by default. The current PostgreSQL defaults are tuned more like a self-managed database than a managed pooled deployment, which makes blue/green-style startup on small poolers fragile.

## What Changes
- Reduce the default PostgreSQL async engine pool footprint when operators have not explicitly configured pool sizing.
- Reduce the default PostgreSQL background-task pool footprint.
- Ensure sync migration/check connections use `NullPool` for PostgreSQL so migration commands do not retain extra pooled slots.
- Add regression coverage for the new PostgreSQL defaults and migration connection behavior.

## Impact
- Affects PostgreSQL deployments only when pool sizing is left at implicit defaults.
- Preserves explicit operator pool settings when `CODEX_LB_DATABASE_POOL_SIZE` or `CODEX_LB_DATABASE_MAX_OVERFLOW` is set.
- Keeps SQLite behavior unchanged.
