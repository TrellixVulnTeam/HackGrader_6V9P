from django.test import TestCase
from django.core.urlresolvers import reverse
import json

from tester.models import Language, TestType


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

    d['code'] = code
    d['test'] = test

    return d

JSON = 'application/json'


class GradeViewTest(TestCase):
    def test_grade_view_with_proper_json(self):
        create_test_types()
        create_languages()
        payload = get_problem()
        d = json.dumps(payload)
        response = self.client.post(reverse('tester:grade'), content_type=JSON, data=d)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], JSON)
