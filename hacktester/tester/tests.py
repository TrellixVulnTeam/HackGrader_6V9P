import json
from faker import Factory

from django.test import override_settings, TestCase
from django.core.urlresolvers import reverse

from .models import Language, TestType

faker = Factory.create()


def create_languages():
    python = Language(name="python")
    python.save()

    ruby = Language(name="ruby")
    ruby.save()


def create_test_types():
    unittest = TestType(value='unittest')
    unittest.save()


def get_problem():
    d = {"test_type": "unittest",
         "language": "python"}

    code = """
def fact(n):
    if n in [0, 1]:
        return 1
    return n * fact(n - 1)
"""

    test = """
import unittest
from solution import fact

class TestStringMethods(unittest.TestCase):
    def test_fact_of_zero(self):
        self.assertEqual(fact(0), 1)

    def test_fact_of_one(self):
        self.assertEqual(fact(1), 1)

    def test_fact_of_five(self):
        self.assertEqual(fact(5), 120)


if __name__ == '__main__':
    unittest.main()
"""

    d['solution'] = code
    d['test'] = test

    return d

JSON = 'application/json'


@override_settings(REQUIRES_API_AUTHENTICATION=False)
class GradeViewTest(TestCase):
    def test_grade_view_with_proper_json(self):
        create_test_types()
        create_languages()
        payload = get_problem()
        d = json.dumps(payload)
        response = self.client.post(reverse('tester:grade'), content_type=JSON, data=d)
        content = json.loads(response.content.decode('utf-8'))

        self.assertEqual(response.status_code, 202)
        self.assertEqual(response['content-type'], JSON)
        self.assertIn('run_id', content)

    def test_grade_view_with_unsupported_language(self):
        create_test_types()
        payload = get_problem()
        d = json.dumps(payload)
        response = self.client.post(reverse('tester:grade'), content_type=JSON, data=d)

        self.assertEqual(response.status_code, 400)

    def test_grade_view_with_unsupported_test_type(self):
        create_languages()
        payload = get_problem()
        d = json.dumps(payload)
        response = self.client.post(reverse('tester:grade'), content_type=JSON, data=d)

        self.assertEqual(response.status_code, 400)

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


class CheckResultViewTest(TestCase):
    def test_check_result_with_nonexistent_run_id(self):
        response = self.client.get(reverse('tester:check_result', args=(1,)))

        self.assertEqual(response.status_code, 404)
