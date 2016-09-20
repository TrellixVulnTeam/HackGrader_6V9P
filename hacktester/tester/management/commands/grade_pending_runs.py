from django.core.management.base import BaseCommand

from hacktester.tester.models import TestRun
from hacktester.tester.tasks import grade_pending_run


class Command(BaseCommand):
    help = 'Run any remained pending runs'

    def handle(self, *args, **options):
        pending_runs = TestRun.objects.filter(status='pending')

        self.stdout.write('{} pending runs.'.format(len(pending_runs)))

        for run in pending_runs:
            self.stdout.write('Queueing: {}'.format(run.id))
            r = grade_pending_run.delay(run.id)
            print('Task id: {}'.format(r.id))
