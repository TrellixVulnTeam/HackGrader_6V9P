from django.apps import AppConfig


class TesterConfig(AppConfig):
    name = 'hacktester.tester'

    def ready(self):
        # flake8: noqa
        import hacktester.tester.signals
