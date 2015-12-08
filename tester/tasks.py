from __future__ import absolute_import
from celery import shared_task

from tester.models import TestRun, RunResult
from HackTester.settings import BASE_DIR

import os
import json


RESULT_STATUSES = {0: "ok", 1: "not_ok", 2: "something_bad"}

FILE_EXTENSIONS = {
    "python": ".py"
}

SANDBOX = 'sandbox/'


def save_input(where, contents):
    path = os.path.join(BASE_DIR, SANDBOX, where)

    with open(path, 'w') as f:
        f.write(contents)


@shared_task
def grade_pending_run(run_id):
    if run_id is None:
        pending_task = TestRun.objects.filter(status='pending').first()
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

    returncode, output = (1, "Not working right now")

    pending_task.status = 'done'
    pending_task.save()

    run_result = RunResult()
    run_result.run = pending_task
    run_result.status = RESULT_STATUSES[returncode]
    run_result.output = output
    run_result.save()

    return run_result.id
