import sys
import requests
import time
import hmac
import hashlib
import json
from urllib.parse import urlparse

from settings import API_KEY, API_SECRET, APIS, DEFAULT_API
from helpers import read_binary_file, output_checking_test_binary

API_URL = APIS[DEFAULT_API]

if len(sys.argv) > 1 and sys.argv[1] in APIS:
    API_URL = APIS[sys.argv[1]]

print("Using API_URL: {}".format(API_URL))

GRADE_PATH = '/grade'
GRADE_URL = API_URL + GRADE_PATH


def get_output_check_python():
    tests = output_checking_test_binary("python")
    data = {"test_type": "output_checking",
            "language": "python",
            "solution": read_binary_file('fixtures/output_check/python/solution.py'),
            "test": tests,
            "extra_options": {
                'archive_test_type': True
            }}

    return data


def get_output_check_ruby():
    tests = output_checking_test_binary("ruby")
    data = {"test_type": "output_checking",
            "language": "ruby",
            "solution": read_binary_file('fixtures/output_check/ruby/solution.rb'),
            "test": tests,
            "extra_options": {
                'archive_test_type': True
            }}

    return data


def get_output_check_binary_java():
    tests = output_checking_test_binary("java")
    data = {"test_type": "output_checking",
            "language": "java",
            "solution": read_binary_file('fixtures/output_check/java/solution.java'),
            "test": tests,
            "extra_options": {
                'archive_test_type': True,
                "class_name": "Factorial"
            }}

    return data


def get_binary_unittest_ruby_problem():
    data = {"test_type": "unittest",
            "language": "ruby",
            "solution": read_binary_file('fixtures/binary/solution.rb'),
            "test": read_binary_file('fixtures/binary/tests.rb'),
            }

    return data


def get_binary_unittest_ruby_problem_with_rubocop_error():
    data = {"test_type": "unittest",
            "language": "ruby",
            "solution": read_binary_file('fixtures/binary/solution_rubocop_error.rb'),
            "test": read_binary_file('fixtures/binary/tests.rb'),
            'extra_options': {
                'lint': True
            }}

    return data


def get_binary_unittest_nodejs_problem():
    data = {"test_type": "unittest",
            "language": "javascript/nodejs",
            "solution": read_binary_file('fixtures/binary/solution.js'),
            "test": read_binary_file('fixtures/binary/tests.js'),
            }

    return data


def get_binary_unittest_python_problem():
    data = {"test_type": "unittest",
            "language": "python",
            "solution": read_binary_file('fixtures/binary/solution.py'),
            "test": read_binary_file('fixtures/binary/tests.py'),
            "extra_options": {
                "lint": True
            }}

    return data


def get_binary_unittest_python_problem_with_flake8_error_and_lint_true():
    data = {"test_type": "unittest",
            "language": "python",
            "solution": read_binary_file('fixtures/binary/solution_flake8_error.py'),
            "test": read_binary_file('fixtures/binary/tests.py'),
            "extra_options": {
                "lint": True
            }}

    return data


def get_binary_unittest_python_problem_with_flake8_error_and_lint_false():
    data = {"test_type": "unittest",
            "language": "python",
            "solution": read_binary_file('fixtures/binary/solution_flake8_error.py'),
            "test": read_binary_file('fixtures/binary/tests.py'),
            "extra_options": {
                "lint": False
            }}

    return data


def get_binary_problem():
    d = {'test_type': 'unittest',
         'language': 'java',
         'solution': read_binary_file('fixtures/binary/solution.jar'),
         'test': read_binary_file('fixtures/binary/tests.jar'),
         'extra_options': {
             'qualified_class_name': 'com.hackbulgaria.grader.Tests'
         }}

    return d


def get_binary_unittest_django_problem():
    data = {"test_type": "unittest",
            "language": "python",
            "solution": read_binary_file('fixtures/binary/django/1/django_project.tar.gz'),
            "test": read_binary_file('fixtures/binary/django/1/tests.tar.gz'),
            "extra_options": {
                'archive_test_type': True,
                'archive_solution_type': True,
                'lint': False,
                'time_limit': 20
            }}

    return data


def get_binary_unittest_django_problem_without_project_requirements():
    data = {"test_type": "unittest",
            "language": "python",
            "solution": read_binary_file('fixtures/binary/django/2/django_project.tar.gz'),
            "test": read_binary_file('fixtures/binary/django/2/tests.tar.gz'),
            "extra_options": {
                'archive_test_type': True,
                'archive_solution_type': True,
                'lint': False,
                'time_limit': 20
            }}

    return data


def get_binary_unittest_django_problem_with_binary_tests_and_archived_solution():
    data = {"test_type": "unittest",
            "language": "python",
            "solution": read_binary_file('fixtures/binary/django/3/django_project.tar.gz'),
            "test": read_binary_file('fixtures/binary/django/3/test.py'),
            "extra_options": {
                'archive_solution_type': True,
                'lint': False,
                'time_limit': 20
            }}

    return data


def get_binary_unittest_python_problem_with_archived_tests_and_binary_solution():
    data = {"test_type": "unittest",
            "language": "python",
            "solution": read_binary_file('fixtures/binary/django/4/solution.py'),
            "test": read_binary_file('fixtures/binary/django/4/tests.tar.gz'),
            "extra_options": {
                'archive_test_type': True,
                'lint': False,
                'time_limit': 20
            }}

    return data


def get_binary_unittest_django_problem_with_requiremets_the_same_as_test_requirements():
    data = {"test_type": "unittest",
            "language": "python",
            "solution": read_binary_file('fixtures/binary/django/5/django_project.tar.gz'),
            "test": read_binary_file('fixtures/binary/django/5/tests.tar.gz'),
            "extra_options": {
                'archive_solution_type': True,
                'archive_test_type': True,
                'lint': False,
                'time_limit': 20
            }}

    return data


def test_fork_bomb():
    data = {"test_type": "unittest",
            "language": "python",
            "solution": read_binary_file('fixtures/fork_bomb.py'),
            "test": read_binary_file('fixtures/binary/tests.py'),
            "extra_options": {
                "lint": True
            }}

    return data


def get_and_update_nonce(resource):
    data = {}
    r = -1

    with open('nonce.json', 'r') as f:
        data = json.load(f)

    if resource not in data:
        r = 1
        data[resource] = [r]
    else:
        r = max(data[resource]) + 1
        data[resource].append(r)

    with open('nonce.json', 'w') as f:
        json.dump(data, f, indent=4)

    return str(r)


def get_headers(body, req_and_resource):
    nonce = get_and_update_nonce(req_and_resource)
    date = time.strftime("%c")
    msg = body + date + nonce
    digest = hmac.new(bytearray(API_SECRET.encode('utf-8')),
                      msg=msg.encode('utf-8'),
                      digestmod=hashlib.sha256).hexdigest()

    request_headers = {'Authentication': digest,
                       'Date': date,
                       'X-API-Key': API_KEY,
                       'X-Nonce-Number': nonce}

    return request_headers


def make_request(problem):
    req_and_resource = "POST {}".format(GRADE_PATH)

    headers = get_headers(json.dumps(problem), req_and_resource)
    r = requests.post(GRADE_URL, json=problem, headers=headers)

    print(r.status_code)  # Should return 202 accepted

    # Returns JSON that looks like this:
    # {"run_id": 2}
    print(r.text)

    if r.status_code not in [200, 202]:
        sys.exit(1)

    print(r.headers['Location'])  # The url for polling
    check_url = r.headers['Location']

    run_id = r.json()['run_id']
    print(run_id)

    path = urlparse(check_url).path
    req_and_resource = "GET {}".format(path)
    r1 = requests.get(check_url, headers=get_headers(path, req_and_resource))

    while r1.status_code == 204:
        print(r1.status_code)
        print(r1.headers['X-Run-Status'])
        r1 = requests.get(check_url, headers=get_headers(path, req_and_resource))
        time.sleep(1)

    r1.text.encode('utf-8', 'ignore')
    print(r1.text)


def main():
    make_request(get_binary_unittest_ruby_problem())
    make_request(get_binary_unittest_ruby_problem_with_rubocop_error())

    make_request(get_binary_unittest_nodejs_problem())

    make_request(get_binary_unittest_python_problem())
    make_request(get_binary_unittest_python_problem_with_flake8_error_and_lint_true())
    make_request(get_binary_unittest_python_problem_with_flake8_error_and_lint_false())
    make_request(get_binary_unittest_python_problem_with_archived_tests_and_binary_solution())

    make_request(get_binary_unittest_django_problem())
    make_request(get_binary_unittest_django_problem_without_project_requirements())
    make_request(get_binary_unittest_django_problem_with_binary_tests_and_archived_solution())
    make_request(get_binary_unittest_django_problem_with_requiremets_the_same_as_test_requirements())

    make_request(get_binary_problem())

    make_request(get_output_check_python())
    make_request(get_output_check_ruby())
    make_request(get_output_check_binary_java())

    make_request(test_fork_bomb())


if __name__ == '__main__':
    main()
