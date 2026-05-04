# Proposal: fix-asyncpg-prepared-statement-cache

## Why

On some Postgres deployments (notably when connecting through a pooler that uses transaction pooling),
`asyncpg`'s prepared statement cache can break and crash the app with an error like:

`DuplicatePreparedStatementError: prepared statement "__asyncpg_stmt_N__" already exists`

This can prevent the service from starting and can also surface as 500s on otherwise unrelated routes.

## What Changes

- Disable asyncpg prepared statement caching by default for `postgresql+asyncpg://` connections by
  setting `prepared_statement_cache_size=0` in SQLAlchemy `connect_args`.

## Impact

- Improves stability for Postgres behind poolers.
- Slightly reduces performance vs prepared statements, but avoids hard failures.

