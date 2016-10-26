from __future__ import absolute_import
import shutil
from subprocess import CalledProcessError, TimeoutExpired
import os

from celery import shared_task
from celery.utils.log import get_task_logger
from celery.exceptions import SoftTimeLimitExceeded

from django.conf import settings

from ..models import RunResult, TestRun

from .test_preparators import PreparatorFactory, FileSystemManager

from .common_utils import get_result_status, get_pending_task
from .docker_utils import (run_code_in_docker, wait_while_docker_finishes, get_output,
                           get_docker_logs, docker_cleanup)

logger = get_task_logger(__name__)

CELERY_TIME_LIMIT_REACHED = """Soft time limit reached while executing run_id:{run_id}"""


@shared_task(bind=True, max_retries=settings.CELERY_TASK_MAX_RETRIES)
def grade_pending_run(self, run_id, input_folder):
    pending_task = get_pending_task(run_id)

    container_id = None
    try:
        container_id = run_code_in_docker(input_folder=input_folder)
        wait_while_docker_finishes(container_id)

        logs = get_docker_logs(container_id)
        logger.info(logs)
        returncode, output = get_output(logs)

    except CalledProcessError as e:
        returncode = e.returncode
        output = repr(e)
    except TimeoutExpired as e:
        returncode = 127
        output = repr(e)
    except SoftTimeLimitExceeded as exc:
        logger.exception(CELERY_TIME_LIMIT_REACHED.format(run_id))
        self.retry(exc=exc)
    finally:
        if container_id:
            docker_cleanup(container_id)

    run_result = RunResult()
    run_result.run = pending_task
    run_result.returncode = returncode
    run_result.status = get_result_status(returncode)
    run_result.output = output
    run_result.save()

    results = RunResult.objects.filter(run=pending_task)

    if results.count() == pending_task.number_of_results:
        pending_task.status = "done"
        pending_task.save()

    return run_result.id


@shared_task(name='clean_up_test_env')
def clean_up_test_env():
    test_folders = [folder for folder in os.listdir(FileSystemManager.SANDBOX) if folder.isdigit()]
    finished_runs = TestRun.objects.filter(pk__in=test_folders, status="done")
    for run in finished_runs:
        shutil.rmtree(os.path.join(FileSystemManager.SANDBOX, str(run.id)))


@shared_task(bind=True, max_retries=settings.CELERY_TASK_MAX_RETRIES)
def prepare_for_grading(self, run_id):
    pending_task = get_pending_task(run_id)
    if pending_task is None:
        return "No tasks to run right now."

    preparator = PreparatorFactory.get(pending_task)
    test_runs = preparator.prepare()
    for data in test_runs:
        grade_pending_run.apply_async((data["run_id"],
                                       data["input_folder"]),
                                      countdown=1)
