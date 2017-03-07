from __future__ import absolute_import
import os
from celery import Celery
from django.apps import AppConfig
from django.conf import settings  # noqa

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')

app = Celery('HackTester')


class CeleryConfig(AppConfig):
    name = 'hacktester'
    verbose_name = 'Celery Config'

    def ready(self):
        app.config_from_object('django.conf:settings', namespace='CELERY')
        app.autodiscover_tasks(lambda: settings.INSTALLED_APPS, force=True)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
