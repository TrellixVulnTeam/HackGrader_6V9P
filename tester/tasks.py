from __future__ import absolute_import
from celery import shared_task

from tester.models import TestRun, RunResult
from HackTester.settings import BASE_DIR

import os
import json

from subprocess import CalledProcessError, check_output, STDOUT, TimeoutExpired

FILE_EXTENSIONS = {
    "python": ".py",
    "ruby": ".rb"
}

SANDBOX = 'sandbox/'

DOCKER_TIMELIMIT = 10
DOCKER_COMMAND = "docker run -v {grader}:/grader -v {sandbox}:/grader/input grader python3 grader/start.py"
DOCKER_COMMAND = DOCKER_COMMAND \
        .format(**{"grader": os.path.join(BASE_DIR, "grader"),
                   "sandbox": os.path.join(BASE_DIR, SANDBOX)})


def save_input(where, contents):
    path = os.path.join(BASE_DIR, SANDBOX, where)

    with open(path, 'w') as f:
        f.write(contents)


def run_code_in_docker():
    json_output = check_output(['/bin/bash', '-c', DOCKER_COMMAND],
                               stderr=STDOUT,
                               shell=False,
                               timeout=DOCKER_TIMELIMIT)

    decoded_output = json.loads(json_output.decode('utf-8'))
    returncode = decoded_output["returncode"]
    output = decoded_output["output"]

    return (returncode, output)


def get_result_status(returncode):
    if returncode == 0:
        return 'ok'

    return 'not_ok'


@shared_task
def grade_pending_run(run_id):
    if run_id is None:
        pending_task = TestRun.objects.filter(status='pending') \
                                      .order_by('-created_at') \
                                      .first()
    else:
        pending_task = TestRun.objects.filter(pk=run_id).first()

    if pending_task is None:
        return "No tasks to run right now."

    language = pending_task.problem_test.language.name.lower()

    pending_task.status = 'running'
    pending_task.save()

    extension = FILE_EXTENSIONS[language]
    solution = 'solution{}'.format(extension)
    tests = 'tests{}'.format(extension)

    save_input(solution, pending_task.code)
    save_input(tests, pending_task.problem_test.code)

    data = {
        'language': language,
        'solution': solution,
        'tests': tests
    }
    save_input('data.json', json.dumps(data))

    try:
        returncode, output = run_code_in_docker()
        status = 'done'
    except CalledProcessError as e:
        returncode = e.returncode
        output = repr(e)
        status = 'failed'
    except TimeoutExpired as e:
        returncode = 127
        output = repr(e)
        status = 'docker_time_limit_hit'

    pending_task.status = status
    pending_task.save()

    run_result = RunResult()
    run_result.run = pending_task
    run_result.status = get_result_status(returncode)
    run_result.output = output
    run_result.save()

    return run_result.id
