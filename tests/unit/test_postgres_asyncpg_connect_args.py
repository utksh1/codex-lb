from __future__ import annotations


def test_postgres_async_connect_args_disables_prepared_statement_cache() -> None:
    # Importing from app.db.session is safe in unit tests because the test suite
    # forces SQLite via CODEX_LB_DATABASE_URL in tests/conftest.py.
    from app.db.session import _postgres_async_connect_args

    assert _postgres_async_connect_args("sqlite+aiosqlite:///./local.db") is None
    assert _postgres_async_connect_args("postgresql+asyncpg://user:pass@host/db") == {
        "prepared_statement_cache_size": 0,
        "statement_cache_size": 0,
    }
