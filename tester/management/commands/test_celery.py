from django.core.management.base import BaseCommand, CommandError
from tester.tasks import add
from celery.result import AsyncResult


class Command(BaseCommand):
    help = "Test Celery"

    def add_arguments(self, parser):
        parser.add_argument('--a', type=int, default=1)
        parser.add_argument('--b', type=int, default=1)
        parser.add_argument('--task_id', type=str, default=None)

    def handle(self, *args, **kwargs):
        if kwargs['task_id'] is None:
            result = add.delay(kwargs['a'], kwargs['b'])
            self.stdout.write(result.id)
        else:
            result = AsyncResult(kwargs['task_id'])
            self.stdout.write(result.status)
            self.stdout.write(str(result.result))
