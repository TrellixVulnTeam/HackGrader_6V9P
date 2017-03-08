import factory
from faker import Factory

from hacktester.tester.models import TestRun, Language, TestType

faker = Factory.create()


class TestTypeFactory(factory.DjangoModelFactory):
    class Meta:
        model = TestType


class LanguageFactory(factory.DjangoModelFactory):
    class Meta:
        model = Language


class TestRunFactory(factory.DjangoModelFactory):
    class Meta:
        model = TestRun

    language = factory.SubFactory(LanguageFactory)
    test_type = factory.SubFactory(TestTypeFactory)
