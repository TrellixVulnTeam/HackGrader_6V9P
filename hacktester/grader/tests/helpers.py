import shutil
import os
from subprocess import check_output, STDOUT, CalledProcessError
import json


from ..settings import INPUT
from django.conf import settings

DATA_FILE = os.path.join(INPUT, 'data.json')
GRADER_APP = os.path.join(str(settings.APPS_DIR), "grader")
FIXTURES = os.path.join(str(settings.APPS_DIR), "grader", "tests", "fixtures")


def copy_fixture(name, extension):
    solution_file = "{}_solution.{}".format(name, extension)
    tests_file = "{}_tests.{}".format(name, extension)

    solution_src = os.path.join(FIXTURES, solution_file)
    solution_dest = os.path.join(INPUT, 'solution.{}'.format(extension))

    test_src = os.path.join(FIXTURES, tests_file)
    test_dest = os.path.join(INPUT, 'tests.{}'.format(extension))

    shutil.copyfile(solution_src, solution_dest)
    shutil.copyfile(test_src, test_dest)


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
    try:
        output = check_output(['python3', GRADER_APP + '/start.py'], stderr=STDOUT).decode('utf-8')
        return output
    except CalledProcessError as e:
        raise


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


def prepare(name, extension, language, copy=False, **kwargs):
    solution_file = 'solution.{}'.format(extension)
    tests_file = 'tests.{}'.format(extension)

    data = {
        'language': language,
        'solution': solution_file,
        'tests': tests_file
    }

    for key, value in kwargs.items():
        data[key] = value

    save_data_json(data)

    if copy is not False:
        copy_fixture(name, extension)
    else:
        fixture = get_fixture(name, extension)
        solution = fixture['solution']
        tests = fixture['tests']

        save_file(solution_file, solution)
        save_file(tests_file, tests)