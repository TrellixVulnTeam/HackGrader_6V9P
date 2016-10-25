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

    cmd_args = sys.argv
    if len(cmd_args) > 1:
        data["cmd_args"] = cmd_args[1:]

    KEYS = ['language', 'solution', 'tests']

    for key in KEYS:
        if key not in data:
            exit_with_error("Key '{}' not set in data.json".format(key))

    Grader = GraderFactory.get_grader(data['language'])

    data['solution'] = os.path.join(INPUT, data['solution'])
    data['tests'] = os.path.join(INPUT, data['tests'])

    prev_dir = os.getcwd()
    os.chdir(INPUT)

    grader = Grader(data)
    returncode, output = grader.run()

    os.chdir(prev_dir)

    result = {
        'returncode': returncode,
        'output': output
    }

    print(json.dumps(result, indent=4))


if __name__ == '__main__':
    main()
