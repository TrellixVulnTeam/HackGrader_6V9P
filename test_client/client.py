import sys
import requests
import time

run_local = False

if len(sys.argv) and sys.argv[1] == 'local':
    run_local = True

if run_local:
    API_URL = 'http://localhost:8000'
else:
    API_URL = 'http://46.101.117.211'

GRADE_URL = API_URL + '/grade'


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

r = requests.post(GRADE_URL, json=get_problem())
print(r.status_code)  # Returns 202 accepted
print(r.headers['Location'])  # The url for polling
check_url = r.headers['Location']

print(r.text)
# Returns JSON that looks like this:
# {"run_id": 2}

run_id = r.json()['run_id']
print(run_id)

r1 = requests.get(check_url)

while r1.status_code == 204:
    print(r1.status_code)
    r1 = requests.get(check_url)
    time.sleep(1)

print(r1.text)
# print(r1.json())
