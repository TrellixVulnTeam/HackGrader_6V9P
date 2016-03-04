import os
import unittest
import contextlib
import json
import glob

from helpers import (call_start, prepare, DATA_FILE, INPUT)


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
        prepare('fact', 'py', 'python')

        output = json.loads(call_start())
        self.assertEqual(0, output['returncode'])
        self.assertIn('OK', output['output'])

    def test_grader_when_test_is_calling_solution_from_check_output(self):
        prepare('derivatives', 'py', 'python')

        output = json.loads(call_start())
        self.assertEqual(0, output['returncode'])
        self.assertIn('OK', output['output'])

    def test_grader_with_while_true_pass_loop(self):
        prepare('while_true', 'py', 'python')

        output = json.loads(call_start())
        self.assertEqual(1, output['returncode'])
        self.assertEqual('Time limit exceeded. Maybe infinite loop?', output['output'])

    def test_grader_with_exec(self):
        prepare('ruby_exec', 'rb', 'ruby')

        output = json.loads(call_start())
        self.assertEqual(1, output['returncode'])

    def test_grader_with_exec_loop(self):
        prepare('exec_loop', 'rb', 'ruby')

        output = json.loads(call_start())
        self.assertEqual(1, output['returncode'])

    def test_grader_with_cyrillic_in_input_ifle(self):
        prepare('cyrillic', 'py', 'python')

        output = json.loads(call_start())
        self.assertEqual(1, output['returncode'])

if __name__ == '__main__':
    unittest.main()
