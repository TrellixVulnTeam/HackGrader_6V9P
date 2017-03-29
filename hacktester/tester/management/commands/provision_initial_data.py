from django.core.management.base import BaseCommand

from hacktester.tester.models import TestType, Language
from hacktester.runner.settings import (OUTPUT_CHECKING, UNITTEST,
                                        JAVA, PYTHON, RUBY, JAVASCRIPT)


TEST_TYPES = [OUTPUT_CHECKING, UNITTEST]

JAVA_EXTENSION = ".java"
PYTHON_EXTENSION = ".py"
RUBY_EXTENSION = ".rb"
JAVASCRIPT_EXTENSION = ".js"
LANGUAGES = (
    (JAVA, JAVA_EXTENSION),
    (PYTHON, PYTHON_EXTENSION),
    (RUBY, RUBY_EXTENSION),
    (JAVASCRIPT, JAVASCRIPT_EXTENSION)
)


class Command(BaseCommand):

    def add_languages(self):
        for language, extension in LANGUAGES:
            if Language.objects.filter(name=language).last() is None:
                Language.objects.create(name=language, extension=extension)

    def add_test_types(self):
        for test_type_value in TEST_TYPES:
            if TestType.objects.filter(value=test_type_value).last() is None:
                TestType.objects.create(value=test_type_value)

    def handle(self, *args, **options):
        self.add_test_types()
        self.add_languages()
