## ADDED Requirements

### Requirement: PostgreSQL default pool sizing remains deploy-safe on managed poolers

When `CODEX_LB_DATABASE_URL` targets PostgreSQL and the operator has not explicitly configured pool sizing, the system MUST use deploy-safe default async engine pool limits that keep startup and steady-state connection pressure low enough for managed session poolers.

#### Scenario: implicit PostgreSQL pool settings use deploy-safe defaults

- **WHEN** `CODEX_LB_DATABASE_URL` points to PostgreSQL
- **AND** `CODEX_LB_DATABASE_POOL_SIZE` is not set
- **AND** `CODEX_LB_DATABASE_MAX_OVERFLOW` is not set
- **THEN** the main async engine uses reduced default pool limits
- **AND** the background async engine also uses reduced default pool limits

#### Scenario: explicit PostgreSQL pool settings preserve operator intent

- **WHEN** `CODEX_LB_DATABASE_URL` points to PostgreSQL
- **AND** the operator explicitly sets `CODEX_LB_DATABASE_POOL_SIZE` and/or `CODEX_LB_DATABASE_MAX_OVERFLOW`
- **THEN** the system uses those explicit values for the main async engine instead of overriding them
