"""Pytest configuration: bootstrap Django settings for template rendering."""

import django
from django.conf import settings


def pytest_configure():
    if not settings.configured:
        settings.configure(
            TEMPLATES=[
                {
                    "BACKEND": "django.template.backends.django.DjangoTemplates",
                    "DIRS": [],
                    "APP_DIRS": False,
                }
            ],
            DEFAULT_AUTO_FIELD="django.db.models.BigAutoField",
        )
        django.setup()
