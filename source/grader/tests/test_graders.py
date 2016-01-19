import os
import unittest
import contextlib
import json
import glob

from helpers import call_start, save_data_json, save_file, DATA_FILE, INPUT


class TestGraders(unittest.TestCase):
    def setUp(self):
        self.cwd = os.getcwd()
        os.chdir('../')

    def tearDown(self):
        os.chdir(self.cwd)

        all_files = glob.glob("{}/*".format(INPUT))
        sample_files = glob.glob("{}/*.sample".format(INPUT))
        created_by_test = set(all_files) - set(sample_files)

        print(created_by_test)
        for path in created_by_test:
            with contextlib.suppress(IsADirectoryError, FileNotFoundError):
                os.remove(path)

    def test_grader_with_python_with_correct_tests_and_solution(self):
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

        data = {
            'language': 'python',
            'solution': 'solution.py',
            'tests': 'tests.py'
        }
        save_data_json(data)
        save_file('solution.py', code)
        save_file('tests.py', test)

        output = json.loads(call_start())
        self.assertEqual(0, output['returncode'])
        self.assertIn('OK', output['output'])

if __name__ == '__main__':
    unittest.main()
