from test_plus.test import TestCase
from hacktester.seed.factories import TestRunFactory
from django.core.cache import cache
from django.conf import settings


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
