from __future__ import absolute_import
import os
import time
import shutil
from subprocess import CalledProcessError, TimeoutExpired, check_output, STDOUT

from celery import shared_task, chain
from celery.utils.log import get_task_logger
from celery.exceptions import SoftTimeLimitExceeded

from django.conf import settings
from django.shortcuts import get_object_or_404

from hacktester.runner import return_codes

from .common_utils import get_result_status, get_pending_task
from .docker_utils import (
    get_output,
    docker_cleanup,
    get_docker_logs,
    run_code_in_docker,
    DOCKER_INSPECT_COMMAND,
)

from ..models import RunResult, TestRun
from ..preparators.factory import PreparatorFactory
from ..preparators.filesystem_manager import FileSystemManager


logger = get_task_logger(__name__)

CELERY_TIME_LIMIT_REACHED = """Soft time limit reached while executing run_id:{run_id}"""


@shared_task(bind=True, max_retries=settings.CELERY_TASK_MAX_RETRIES, time_limit=40)
def has_docker_finished(self, run_id, container_id):
    keys = {"container_id": container_id,
            "state": "{{.State.Running}}"}
    command = DOCKER_INSPECT_COMMAND.format(**keys)

    result = None
    try:
        result = check_output(['/bin/bash', '-c', command],
                              stderr=STDOUT).decode('utf-8').strip()
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

    logger.info("Checking if {} has finished: {}".format(container_id, result))

    while True:
        if result == 'true':
            time.sleep(1)
            try:
                result = check_output(['/bin/bash', '-c', command],
                                      stderr=STDOUT).decode('utf-8').strip()
                logger.info("Checking if {} has finished: {}".format(container_id, result))
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
        else:
            try:
                logs = get_docker_logs(container_id)
                logger.info(logs)
                returncode, output = get_output(logs)
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
            finally:
                if container_id:
                    docker_cleanup(container_id)
                break

    pending_task = get_object_or_404(TestRun, id=run_id)
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


@shared_task(bind=True, max_retries=settings.CELERY_TASK_MAX_RETRIES, time_limit=40)
def grade_pending_run(self, run_id, input_folder):
    container_id = None
    try:
        container_id = run_code_in_docker(input_folder=input_folder)
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

    sig = has_docker_finished.s(run_id, container_id)
    finished = sig.delay()
    result = None
    while True:
        if finished.result:
            result = finished.result
            break
        else:
            sig.set(countdown=1)
    return result


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
        grade = grade_pending_run.s(**data).set(countdown=1)
        clean = clean_up_after_run.s()

        tasks = chain(grade, clean)
        tasks()
