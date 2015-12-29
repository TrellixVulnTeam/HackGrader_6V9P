import requests

API_URL = 'http://46.101.117.211'
GRADE_URL = API_URL + '/grade'
CHECK_RESULT_URL = API_URL + "/check_result"


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
print(r.text)

# Returns JSON that looks like this:
# {"run_id": 2}

run_id = r.json()['run_id']
print(run_id)

r1 = requests.get(CHECK_RESULT_URL, params={'run_id': run_id})

while r1.status_code == 204:
    print(r1.status_code)
    # print(r1.json()['status'])
    r1 = requests.get(CHECK_RESULT_URL, params={'run_id': run_id})

print(r1.text)
# print(r1.json())
