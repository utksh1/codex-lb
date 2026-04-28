## 1. Spec
- [x] 1.1 Add a `database-backends` delta covering deploy-safe PostgreSQL default pool sizing.
- [x] 1.2 Add a `database-migrations` delta covering unpooled PostgreSQL sync migration connections.

## 2. Implementation
- [x] 2.1 Apply deploy-safe default PostgreSQL pool sizing only when pool settings are not explicitly configured.
- [x] 2.2 Reduce the PostgreSQL background-task pool footprint.
- [x] 2.3 Use `NullPool` for PostgreSQL sync migration/check engine creation.

## 3. Validation
- [x] 3.1 Add targeted unit coverage for PostgreSQL settings defaults and migration sync engine configuration.
- [x] 3.2 Run focused pytest coverage for DB settings/session/migration behavior.
