from django.core.management.base import BaseCommand

from hacktester.api_auth.models import ApiUser


class Command(BaseCommand):
    help = 'Create new API user'

    def add_arguments(self, parser):
        parser.add_argument('host', type=str)

    def handle(self, *args, **options):
        host = options['host']
        user = ApiUser.create_api_user(host=host)
        self.stdout.write("Key: {}".format(user.key))
        self.stdout.write("Secret: {}".format(user.secret))
