import os
import unittest
import json
from subprocess import CalledProcessError
import contextlib

from .helpers import save_data_json, call_start, DATA_FILE


class TestGraderStart(unittest.TestCase):
    def setUp(self):
        self.cwd = os.getcwd()
        os.chdir('../')

    def tearDown(self):
        os.chdir(self.cwd)
        with contextlib.suppress(FileNotFoundError):
            os.remove(DATA_FILE)

    def test_start_with_no_data_json(self):
        with self.assertRaises(CalledProcessError) as cm:
            call_start()

        expected_output = {
            'error': 'Cannot find {}'.format(DATA_FILE)
        }

        output = json.loads(cm.exception.output.decode('utf-8'))
        self.assertEqual(expected_output, output)

    def test_start_with_no_language_key_in_data_json(self):
        data = {}
        save_data_json(data)

        with self.assertRaises(CalledProcessError) as cm:
            call_start()

        expected_output = {
            'error': "Key 'language' not set in data.json"
        }
        output = json.loads(cm.exception.output.decode('utf-8'))
        self.assertEqual(expected_output, output)

    def test_start_with_not_present_solution_file(self):
        data = {
            'language': 'python',
        }
        save_data_json(data)

        with self.assertRaises(CalledProcessError) as cm:
            call_start()

        expected_output = {
            'error': "Key 'solution' not set in data.json"
        }
        output = json.loads(cm.exception.output.decode('utf-8'))
        self.assertEqual(expected_output, output)

    def test_start_with_not_present_tests_file(self):
        data = {
            'language': 'python',
            'solution': 'solution.py'
        }
        save_data_json(data)

        with self.assertRaises(CalledProcessError) as cm:
            call_start()

        expected_output = {
            'error': "Key 'tests' not set in data.json"
        }
        output = json.loads(cm.exception.output.decode('utf-8'))
        self.assertEqual(expected_output, output)
