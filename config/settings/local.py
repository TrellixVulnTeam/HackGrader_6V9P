# flake8: noqa
"""
Local settings

- Run in Debug mode
- Use console backend for emails
- Add Django Debug Toolbar
- Add django-extensions as app
"""

from .common import *  # noqa

# DEBUG
# ------------------------------------------------------------------------------
DEBUG = env.bool('DJANGO_DEBUG', default=True)
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

# SECRET CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Note: This key only used for development and testing.
SECRET_KEY = env('DJANGO_SECRET_KEY', default='23g#m5uc&4^!ji!*4z4cnh*56yhwjz*t5m35)+!dn7^ljqc2zc')

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

# For remote debugger for celery
CELERY_RDBSIG = 1
