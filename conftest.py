import os

import pytest
from django.conf import settings
from django.db import connections

SAFE_TEST_DB_HOSTS = {"localhost", "127.0.0.1", ""}


def pytest_sessionstart(session):
    if os.environ.get("ALLOW_NON_LOCAL_DB_FOR_TESTS"):
        return
    # Inspect all configured DB connections
    for alias in connections:
        conn_settings = settings.DATABASES[alias]
        host = conn_settings.get("HOST") or ""
        if host not in SAFE_TEST_DB_HOSTS:
            pytest.exit(
                f"Refusing to run tests against non-local database host '{host}' (alias '{alias}'). Set ALLOW_NON_LOCAL_DB_FOR_TESTS=1 to override.",
                returncode=1,
            )
