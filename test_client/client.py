import sys
import requests
import time
import hmac
import hashlib
import json

from settings import API_KEY, API_SECRET


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


def get_and_update_nonce():
    used = []
    r = -1

    with open('nonce.json', 'r') as f:
        used = json.load(f)
        if len(used) == 0:
            r = 1
        else:
            r = max(used) + 1

        used.append(r)

    with open('nonce.json', 'w') as f:
        json.dump(used, f)

    return str(r)


def get_headers():
    nonce = get_and_update_nonce()
    date = time.strftime("%c")
    body = json.dumps(get_problem())
    msg = body + date + nonce
    digest = hmac.new(bytearray(API_SECRET.encode('utf-8')),
                      msg=msg.encode('utf-8'),
                      digestmod=hashlib.sha256).hexdigest()

    request_headers = {'Authentication': digest,
                       'Date': date,
                       'X-API-Key': API_KEY,
                       'X-Nonce-Number': nonce}

    return request_headers

run_local = False

if len(sys.argv) > 1 and sys.argv[1] == 'local':
    run_local = True

if run_local:
    API_URL = 'http://localhost:8000'
else:
    API_URL = 'http://46.101.117.211'

GRADE_URL = API_URL + '/grade'


r = requests.post(GRADE_URL, json=get_problem(), headers=get_headers())

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

r1 = requests.get(check_url)

while r1.status_code == 204:
    print(r1.status_code)
    print(r1.headers['X-Run-Status'])
    r1 = requests.get(check_url)
    time.sleep(1)

print(r1.text)
