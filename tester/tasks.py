from __future__ import absolute_import
from celery import shared_task

from tester.models import TestRun, RunResult

# from grader.grader_factory import GraderFactory


RESULT_STATUSES = {0: "ok", 1: "not_ok", 2: "something_bad"}


@shared_task
def grade_pending_run(run_id):
    if run_id is None:
        pending_task = TestRun.objects.filter(status='pending').first()
    else:
        pending_task = TestRun.objects.filter(pk=run_id).first()

    if pending_task is None:
        return "No tasks to run right now."

    language = pending_task.problem_test.language.name
    # Grader = GraderFactory.get_grader(language)

    pending_task.status = 'running'
    pending_task.save()

    # grader = Grader(code_under_test=pending_task.code,
                  # tests=pending_task.problem_test.code)
    # returncode, output = grader.run_code()
    returncode, output = (1, "Not working right now")

    pending_task.status = 'done'
    pending_task.save()

    run_result = RunResult()
    run_result.run = pending_task
    run_result.status = RESULT_STATUSES[returncode]
    run_result.output = output
    run_result.save()

    return run_result.id
