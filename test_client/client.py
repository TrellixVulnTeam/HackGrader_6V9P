import sys
import requests
import time
import hmac
import hashlib
import json
from urllib.parse import urlparse

from settings import API_KEY, API_SECRET, APIS, DEFAULT_API


def get_problem():
    d = {"test_type": "unittest",
         "language": "python"}

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

    d['code'] = code
    d['test'] = test

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

API_URL = APIS[DEFAULT_API]

if len(sys.argv) > 1 and sys.argv[1] in APIS:
    API_URL = APIS[sys.argv[1]]

print("Using API_URL: {}".format(API_URL))

GRADE_PATH = '/grade'
GRADE_URL = API_URL + GRADE_PATH

req_and_resource = "POST {}".format(GRADE_PATH)
headers = get_headers(json.dumps(get_problem()), req_and_resource)
r = requests.post(GRADE_URL, json=get_problem(), headers=headers)

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
