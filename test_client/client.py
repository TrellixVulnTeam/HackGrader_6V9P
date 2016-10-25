import sys
import requests
import time
import hmac
import hashlib
import json
from urllib.parse import urlparse

from settings import API_KEY, API_SECRET, APIS, DEFAULT_API
from helpers import read_file, read_binary_file, output_checking_test_binary

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
            "file_type": "plain",
            "code": read_file('fixtures/output_check/python/solution.py'),
            "test": tests,
            "extra_options": {
                "archive_type": "tar_gz"
            }}

    return data


def get_output_check_ruby():
    tests = output_checking_test_binary("ruby")
    data = {"test_type": "output_checking",
            "language": "ruby",
            "file_type": "plain",
            "code": read_file('fixtures/output_check/ruby/solution.rb'),
            "test": tests,
            "extra_options": {
                "archive_type": "tar_gz"
            }}

    return data


def get_plain_java_output_checking_problem():
    tests = output_checking_test_binary("ruby")
    data = {"test_type": "output_checking",
            "language": "java plain",
            "file_type": 'plain',
            "code": read_file('fixtures/output_check/java/solution.java'),
            "test": tests,
            "extra_options": {
                "archive_type": "tar_gz",
                "class_name": "Factorial"
            }}

    return data


def get_plain_ruby_problem():
    data = {"test_type": "unittest",
            "language": "ruby",
            "file_type": 'plain',
            "code": read_file('fixtures/plain/solution.rb'),
            "test": read_file('fixtures/plain/tests.rb'),
            }

    return data


def get_plain_python_problem():
    data = {"test_type": "unittest",
            "language": "python",
            "file_type": 'plain',
            "code": read_file('fixtures/plain/solution.py'),
            "test": read_file('fixtures/plain/tests.py'),
            "extra_options": {
                "foo": "bar"    # wtf? lol
            }}

    return data


def get_binary_problem():
    d = {'test_type': 'unittest',
         'language': 'java',
         'file_type': 'binary',
         'code': read_binary_file('fixtures/binary/solution.jar'),
         'test': read_binary_file('fixtures/binary/tests.jar'),
         'extra_options': {
             'qualified_class_name': 'com.hackbulgaria.grader.Tests'
          }}

    return d


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

    print(r1.text)


def main():
    make_request(get_plain_ruby_problem())
    make_request(get_plain_python_problem())
    make_request(get_binary_problem())
    make_request(get_output_check_python())
    make_request(get_output_check_ruby())
    #make_request(get_plain_java_output_checking_problem())

if __name__ == '__main__':
    main()
