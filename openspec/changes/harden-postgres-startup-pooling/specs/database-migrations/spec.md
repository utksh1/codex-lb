## ADDED Requirements

### Requirement: PostgreSQL sync migration connections do not retain pooled slots

When Alembic inspection, upgrade, or drift-check code opens synchronous PostgreSQL connections, the system MUST avoid retaining pooled connection slots across those short-lived commands.

#### Scenario: sync PostgreSQL migration engine uses null pooling

- **WHEN** migration tooling opens a synchronous SQLAlchemy engine for a PostgreSQL database URL
- **THEN** it uses `NullPool`
- **AND** each command disposes the engine after the short-lived operation completes
