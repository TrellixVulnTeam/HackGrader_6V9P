from __future__ import absolute_import
import os
import shutil
from subprocess import CalledProcessError, TimeoutExpired

from celery import shared_task
from celery.utils.log import get_task_logger
from celery.exceptions import SoftTimeLimitExceeded

from django.conf import settings
from hacktester.runner import return_codes

from .common_utils import get_result_status, get_pending_task
from .docker_utils import (
    get_output,
    docker_cleanup,
    get_docker_logs,
    run_code_in_docker,
    get_and_call_poll_command,
)
from ..exceptions import PollingError

from ..models import RunResult, TestRun
from ..preparators.factory import PreparatorFactory
from ..preparators.filesystem_manager import FileSystemManager


logger = get_task_logger(__name__)

CELERY_TIME_LIMIT_REACHED = """Soft time limit reached while executing run_id:{run_id}"""


@shared_task(bind=True)
def finish_run(self, pending_task_id, returncode, output):
    pending_task = TestRun.objects.get(id=pending_task_id)
    run_result = RunResult.objects.create(
        run=pending_task,
        returncode=returncode,
        status=get_result_status(returncode),
        output=output
    )

    results = RunResult.objects.filter(run=pending_task)

    if results.count() == pending_task.number_of_results:
        pending_task.status = "done"
        pending_task.save()

    clean_up_after_run.s(run_result.id).set(countdown=1).delay()

    return run_result.id


@shared_task(bind=True, max_retries=settings.CELERY_TASK_MAX_POLLING_RETRIES)
def poll_docker(self, run_id, container_id):
    pending_task = TestRun.objects.get(id=run_id)

    try:
        result = get_and_call_poll_command(container_id)
        logger.info("Checking if {} has finished: {}".format(container_id, result))
        if result == 'true':
            raise PollingError
        logs = get_docker_logs(container_id)
        logger.info(logs)
        returncode, output = get_output(logs)
        if container_id:
            docker_cleanup(container_id)
    except PollingError as exc:
        self.retry(exc=exc, countdown=1)
    except CalledProcessError as e:
        returncode = return_codes.CALLED_PROCESS_ERROR
        output = repr(e)
    except TimeoutExpired as e:
        returncode = return_codes.TIME_LIMIT_ERROR
        output = repr(e)
    except SoftTimeLimitExceeded as exc:
        logger.exception(CELERY_TIME_LIMIT_REACHED.format(run_id))
        self.retry(exc=exc)
    except Exception as e:
        returncode = return_codes.UNKNOWN_EXCEPTION
        output = repr(e)

    return finish_run.s(pending_task.id, returncode, output).delay()


@shared_task(bind=True, max_retries=settings.CELERY_TASK_MAX_RETRIES)
def grade_pending_run(self, run_id, input_folder):
    container_id = None
    returncode = output = None
    pending_task = TestRun.objects.get(id=run_id)
    print(f"DOCKER IMAGE IS {settings.DOCKER_IMAGES.get(pending_task.language.name)}")
    try:
        container_id = run_code_in_docker(input_folder=input_folder, docker_image=pending_task.language.name)
    except CalledProcessError as e:
        returncode = return_codes.CALLED_PROCESS_ERROR
        output = repr(e)
    except TimeoutExpired as e:
        returncode = return_codes.TIME_LIMIT_ERROR
        output = repr(e)
    except SoftTimeLimitExceeded as exc:
        logger.exception(CELERY_TIME_LIMIT_REACHED.format(run_id))
        self.retry(exc=exc)
    except Exception as e:
        returncode = return_codes.UNKNOWN_EXCEPTION  # noqa
        output = repr(e)  # noqa

    pending_task.container_id = container_id
    pending_task.save()

    if returncode is not None and output is not None:
        return finish_run.s(pending_task.id, returncode, output).delay()

    return poll_docker.s(run_id, container_id).delay()


@shared_task
def clean_up_after_run(result_id):
    result = RunResult.objects.get(pk=result_id)
    run = result.run

    if run.status == 'done':
        print('Cleaning up after run {}'.format(run.id))
        try:
            shutil.rmtree(os.path.join(FileSystemManager.SANDBOX, str(run.id)))
        except FileNotFoundError as e:
            logger.info('environment for run {} is clean'.format(run.id))


@shared_task(bind=True, max_retries=settings.CELERY_TASK_MAX_RETRIES)
def prepare_for_grading(self, run_id):
    pending_task = get_pending_task(run_id)

    if pending_task is None:
        return "No tasks to run right now."

    preparator = PreparatorFactory.get(pending_task)
    test_runs = preparator.prepare()

    pending_task.status = 'running'
    pending_task.number_of_results = len(test_runs)
    pending_task.save()

    for data in test_runs:
        grade_pending_run.s(**data).set(countdown=1).delay()
