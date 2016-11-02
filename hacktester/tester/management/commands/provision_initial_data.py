from django.core.management.base import BaseCommand

from hacktester.tester.models import ArchiveType, TestType, Language
from hacktester.runner.settings import (OUTPUT_CHECKING, UNITTEST,
                                        JAVA, PYTHON, RUBY)


TEST_TYPES = [OUTPUT_CHECKING, UNITTEST]

JAVA_EXTENSION = ".java"
PYTHON_EXTENSION = ".py"
RUBY_EXTENSION = ".rb"
LANGUAGES = (
    (JAVA, JAVA_EXTENSION),
    (PYTHON, PYTHON_EXTENSION),
    (RUBY, RUBY_EXTENSION)
)

ARCHIVE_TYPES = ("tar_gz",)


class Command(BaseCommand):
    def add_archive_types(self):
        for archive_type in ARCHIVE_TYPES:
            if ArchiveType.objects.filter(value=archive_type).last() is None:
                ArchiveType.objects.create(value=archive_type)

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
        self.add_archive_types()
