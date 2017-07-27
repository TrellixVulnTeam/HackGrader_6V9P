from test_plus import TestCase
from faker import Factory

from django.core.exceptions import ValidationError

from hacktester.tester.factories import TestRunFactory

faker = Factory.create()


class TestRunFactoryTests(TestCase):
    def test_run_factory_raises_validation_error_on_extra_options_that_is_not_dict(self):
        data = {
            "test_type": faker.text(),
            "language": faker.text(),
            "solution": faker.text(),
            "test": faker.text(),
            "extra_options": faker.text()
        }

        with self.assertRaises(ValidationError):
            TestRunFactory.create_run(data)
