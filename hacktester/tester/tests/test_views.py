import json

from test_plus.test import TestCase

from faker import Factory

from django.test.utils import override_settings
from django.core.cache import cache
from django.conf import settings
from django.urls import reverse

from hacktester.seed.factories import TestRunFactory
from hacktester.tester.models import Language, TestType

faker = Factory.create()


def create_languages():
    python = Language(name="python")
    python.save()

    ruby = Language(name="ruby")
    ruby.save()


def create_test_types():
    unittest = TestType(value='unittest')
    unittest.save()

JSON = 'application/json'


class TestIndexPage(TestCase):

    def setUp(self):
        settings.CACHE_TIMEOUT = 1
        self.url = self.reverse('tester:index')

    def test_index_page_is_cached(self):
        self.assertEqual(len(cache._cache.keys()), 0)
        response = self.client.get(self.url)
        self.response_200(response)
        self.assertNotEqual(len(cache._cache.keys()), 0)

    def test_cache_is_deleted_when_test_run_is_created(self):
        # 1. Access index page.
        self.assertEqual(len(cache._cache.keys()), 0)
        response = self.client.get(self.url)
        self.response_200(response)

        # 2. Assert index page is cached.
        self.assertNotEqual(len(cache._cache.keys()), 0)

        # 3. Create TestRun instance.
        TestRunFactory()

        # 4. Assert cache is deleted.
        self.assertEqual(len(cache._cache.keys()), 0)

    def tearDown(self):
        cache.clear()


class GradeApiTests(TestCase):
    @override_settings(REQUIRES_API_AUTHENTICATION=False)
    def test_grade_does_not_accept_extra_options_different_than_dict(self):
        create_languages()
        create_test_types()
        data = {
            "language": "ruby",
            "test_type": "unittest",
            "extra_options": faker.word()
        }
        d = json.dumps(data)
        response = self.client.post(reverse("tester:grade"), data=d, content_type=JSON)
        self.assertEqual(response.status_code, 400)
