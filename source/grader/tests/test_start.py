import sys
import os
import unittest
import json
from subprocess import check_output, STDOUT, CalledProcessError
import contextlib

sys.path.append('../')
from settings import INPUT

DATA_FILE = os.path.join(INPUT, 'data.json')


def call_start(args=None):
    return check_output(['python3', 'start.py'], stderr=STDOUT)


def save_data_json(data):
    with open(DATA_FILE, 'w') as f:
        f.write(json.dumps(data))


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
        pass

    def test_start_with_not_present_tests_file(self):
        pass

if __name__ == '__main__':
    unittest.main()
