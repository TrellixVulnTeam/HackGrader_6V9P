import os
import unittest
import contextlib
import json
import glob

from helpers import call_start, save_data_json, save_file, get_fixture,\
        DATA_FILE, INPUT


class TestGraders(unittest.TestCase):
    def setUp(self):
        self.cwd = os.getcwd()
        os.chdir('../')

    def tearDown(self):
        os.chdir(self.cwd)

        all_files = glob.glob("{}/*".format(INPUT))
        sample_files = glob.glob("{}/*.sample".format(INPUT))
        created_by_test = set(all_files) - set(sample_files)

        for path in created_by_test:
            with contextlib.suppress(IsADirectoryError, FileNotFoundError):
                os.remove(path)

    def test_grader_with_python_with_correct_tests_and_solution(self):
        fixture = get_fixture('fact', 'py')
        solution = fixture['solution']
        tests = fixture['tests']

        data = {
            'language': 'python',
            'solution': 'solution.py',
            'tests': 'tests.py'
        }
        save_data_json(data)
        save_file('solution.py', solution)
        save_file('tests.py', tests)

        output = json.loads(call_start())
        self.assertEqual(0, output['returncode'])
        self.assertIn('OK', output['output'])

    def test_grader_when_test_is_calling_solution_from_check_output(self):
        fixture = get_fixture('derivatives', 'py')
        solution = fixture['solution']
        tests = fixture['tests']

        data = {
            'language': 'python',
            'solution': 'solution.py',
            'tests': 'tests.py'
        }
        save_data_json(data)
        save_file('solution.py', solution)
        save_file('tests.py', tests)

        output = json.loads(call_start())
        self.assertEqual(0, output['returncode'])
        self.assertIn('OK', output['output'])


if __name__ == '__main__':
    unittest.main()
