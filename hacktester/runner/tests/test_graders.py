import os
import unittest
import contextlib
import json
import glob

from hacktester.runner.settings import TIMELIMIT_EXCEEDED_ERROR
from hacktester.runner.return_codes import TIME_LIMIT_ERROR, WRONG_ANSWER, OK
from .helpers import (call_start, prepare, INPUT)


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
        prepare('fact', 'py', 'python', 'unittest')
        output = json.loads(call_start())
        self.assertEqual(OK, output['returncode'])
        self.assertIn('OK', output['output'])

    def test_grader_when_test_is_calling_solution_from_check_output(self):
        prepare('derivatives', 'py', 'python', 'unittest')

        output = json.loads(call_start())
        self.assertEqual(OK, output['returncode'])
        self.assertIn('OK', output['output'])

    def test_grader_with_while_true_pass_loop(self):
        prepare('while_true', 'py', 'python', 'unittest')

        output = json.loads(call_start())
        self.assertEqual(TIME_LIMIT_ERROR, output['returncode'])
        self.assertEqual(TIMELIMIT_EXCEEDED_ERROR, output['output'])

    def test_grader_with_exec(self):
        prepare('ruby_exec', 'rb', 'ruby', 'unittest')

        output = json.loads(call_start())
        self.assertEqual(WRONG_ANSWER, output['returncode'])

    def test_grader_with_exec_loop(self):
        prepare('exec_loop', 'rb', 'ruby', 'unittest')

        output = json.loads(call_start())
        self.assertEqual(TIME_LIMIT_ERROR, output['returncode'])

    def test_grader_with_cyrillic_in_input_ifle(self):
        prepare('cyrillic', 'py', 'python', 'unittest')

        output = json.loads(call_start())
        self.assertEqual(WRONG_ANSWER, output['returncode'])

    def test_java_junit_jar_grader(self):
        prepare('add', 'jar', 'java', 'unittest', copy=True, qualified_class_name='com.hackbulgaria.grader.Tests')

        output = json.loads(call_start())
        self.assertEqual(OK, output['returncode'])

    def test_grader_with_nodejs_with_correct_testes_and_solution(self):
        prepare('firstElement', 'js', 'nodejs', 'unittest')

        output = json.loads(call_start())
        self.assertEqual(OK, output['returncode'])
