from django.core.management.base import BaseCommand, CommandError
from tester.models import TestRun


class Command(BaseCommand):
    help = "Grade one pending task"

    def handle(self, *args, **kwargs):
        run = TestRun.objects.filter(status='pending').first()

        if run is None:
            self.stdout.write("There are no pending runs at the moment.")
            return

        self.stdout.write(run.problem_test.language.name)
