from phishhunter.db.database import _normalize_database_url


def test_postgres_provider_urls_use_psycopg3_driver():
    assert _normalize_database_url("postgres://user:pass@db.example.test/app")[0] == (
        "postgresql+psycopg://user:pass@db.example.test/app"
    )
    assert _normalize_database_url("postgresql://user:pass@db.example.test/app?sslmode=require")[0] == (
        "postgresql+psycopg://user:pass@db.example.test/app?sslmode=require"
    )
    assert _normalize_database_url("postgresql+psycopg2://user:pass@db.example.test/app")[0] == (
        "postgresql+psycopg://user:pass@db.example.test/app"
    )


def test_upload_limits_are_configurable():
    from phishhunter.config import settings

    assert settings.max_upload_mb >= 7
    assert settings.max_upload_batch_mb >= settings.max_upload_mb
