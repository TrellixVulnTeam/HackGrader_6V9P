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
            ArchiveType.objects.create(value=archive_type)

    def add_languages(self):
        for language, extension in LANGUAGES:
            Language.objects.create(name=language, extension=extension)

    def add_test_types(self):
        for test_type_value in TEST_TYPES:
            TestType.objects.create(value=test_type_value)

    def handle(self):
        self.add_test_types()
