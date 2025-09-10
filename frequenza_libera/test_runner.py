import os

from django.conf import settings
from django.db import connections
from django.test.runner import DiscoverRunner

SAFE_TEST_DB_HOSTS = {"localhost", "127.0.0.1", "", None}


class SafeTestRunner(DiscoverRunner):
    """Test runner that aborts if DB host is non-local to avoid destructive ops on remote DB.

    Override with environment variable ALLOW_NON_LOCAL_DB_FOR_TESTS=1.
    """

    def setup_databases(self, **kwargs):  # noqa: D401
        if not os.environ.get("ALLOW_NON_LOCAL_DB_FOR_TESTS"):
            offenders = []
            for alias in connections:
                cfg = settings.DATABASES[alias]
                host = cfg.get("HOST")
                if host not in SAFE_TEST_DB_HOSTS:
                    offenders.append((alias, host))
            if offenders:
                details = ", ".join(f"{a}:{h}" for a, h in offenders)
                raise SystemExit(
                    f"Refusing to run tests against non-local DB host(s): {details}. "
                    "Set ALLOW_NON_LOCAL_DB_FOR_TESTS=1 to override or point DATABASE_URL to a local/ephemeral DB."
                )
        return super().setup_databases(**kwargs)
