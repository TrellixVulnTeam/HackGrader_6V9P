import json
import sys
import os
from settings import INPUT
from grader_factory import GraderFactory


def main():
    data_file = os.path.join(INPUT, 'data.json')

    if not os.path.exists(data_file):
        # TODO - Log errors somewhere
        print("Cannot located {}".format(data_file), file=sys.stderr)
        sys.exit(1)

    with open(data_file) as f:
        data = json.load(f)

    if 'language' not in data:
        print('There is no language set in {}'.format(data_file),
              file=sys.stderr)

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
