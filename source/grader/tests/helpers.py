import sys
import os
from subprocess import check_output, STDOUT
import json

sys.path.append('../')
from settings import INPUT

# BASE_DIR = os.path.dirname(os.path.abspath("../"))
# print(BASE_DIR)
# INPUT = os.path.join(BASE_DIR, 'input/')
DATA_FILE = os.path.join(INPUT, 'data.json')
FIXTURES = os.path.join("tests", "fixtures")


def get_fixture(name, extension):
    solution_file = "{}_solution.{}".format(name, extension)
    tests_file = "{}_tests.{}".format(name, extension)

    result = {
        "solution": "",
        "tests": ""
    }

    result['solution'] = read_file(os.path.join(FIXTURES, solution_file))
    result['tests'] = read_file(os.path.join(FIXTURES, tests_file))

    return result


def call_start():
    return check_output(['python3', 'start.py'], stderr=STDOUT).decode('utf-8')


def save_data_json(data):
    with open(DATA_FILE, 'w') as f:
        f.write(json.dumps(data))


def save_file(name, code):
    path = os.path.join(INPUT, name)

    with open(path, 'w') as f:
        f.write(code)


def read_file(path):
    contents = ""

    with open(path, 'r') as f:
        contents = f.read()

    return contents


def prepare(name, extension, language):
    fixture = get_fixture(name, extension)

    solution_file = 'solution.{}'.format(extension)
    solution = fixture['solution']

    tests_file = 'tests.{}'.format(extension)
    tests = fixture['tests']

    data = {
        'language': language,
        'solution': solution_file,
        'tests': tests_file
    }

    save_data_json(data)
    save_file(solution_file, solution)
    save_file(tests_file, tests)
