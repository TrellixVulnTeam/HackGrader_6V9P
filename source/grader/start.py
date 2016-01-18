import json
import sys
import os
from settings import INPUT
from grader_factory import GraderFactory


def exit_with_error(desc):
    error_dict = {
        'error': desc
    }

    print(json.dumps(error_dict), file=sys.stderr)
    sys.exit(1)


def main():
    data_file = os.path.join(INPUT, 'data.json')

    if not os.path.exists(data_file):
        exit_with_error("Cannot find {}".format(data_file))

    with open(data_file) as f:
        data = json.load(f)

    if 'language' not in data:
        exit_with_error("Key 'language' not set in data.json")

    Grader = GraderFactory.get_grader(data['language'])
    solution = os.path.join(INPUT, data['solution'])
    tests = os.path.join(INPUT, data['tests'])

    grader = Grader(solution, tests)
    returncode, output = grader.run_code()

    result = {
        'returncode': returncode,
        'output': output
    }

    print(json.dumps(result, indent=4))


if __name__ == '__main__':
    main()
