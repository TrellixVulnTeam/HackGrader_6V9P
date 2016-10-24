from __future__ import absolute_import
import time
import shutil
from subprocess import CalledProcessError, TimeoutExpired

from celery import shared_task
from celery.utils.log import get_task_logger
from celery.exceptions import SoftTimeLimitExceeded

from django.conf import settings

from .test_preparators import (FileSystemManager, prepare_unittest,
                               prepare_output_checking_environment,
                               prepare_output_test)
from .models import  RunResult
from .utils import get_result_status, get_pending_task
from .docker_utils import (run_code_in_docker, wait_while_docker_finishes, get_output,
                           get_docker_logs, docker_cleanup)

logger = get_task_logger(__name__)

CELERY_TIME_LIMIT_REACHED = """Soft time limit reached while executing \
                               language:{language}, \
                               solution:{solution}, test:{tests}"""


@shared_task(bind=True, max_retries=settings.CELERY_TASK_MAX_RETRIES)
def run_test(self, run_id, data, input_folder):
    pending_task = get_pending_task(run_id)

    container_id = None
    try:
        container_id = run_code_in_docker(input_folder=input_folder)
        wait_while_docker_finishes(container_id)

        logs = get_docker_logs(container_id)
        logger.info(logs)
        returncode, output = get_output(logs)

        status = 'done'
    except CalledProcessError as e:
        returncode = e.returncode
        output = repr(e)
        status = 'failed'
    except TimeoutExpired as e:
        returncode = 127
        output = repr(e)
        status = 'docker_time_limit_hit'
    except SoftTimeLimitExceeded as exc:
        logger.exception(CELERY_TIME_LIMIT_REACHED.format(**data))
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
    return run_result.id


@shared_task
def clean_up_test_env(run_id, test_folder):
    while True:
        pending_task = get_pending_task(run_id)
        results = RunResult.objects.filter(run=pending_task)
        if len(results) == pending_task.number_of_results:
            shutil.rmtree(test_folder)
            pending_task.status = "done"
            pending_task.save()
            break
        time.sleep(2)


@shared_task(bind=True, max_retries=settings.CELERY_TASK_MAX_RETRIES)
def grade_pending_run(self, run_id):
    pending_task = get_pending_task(run_id)
    if pending_task is None:
        return "No tasks to run right now."

    language = pending_task.language.name.lower()
    test_type = pending_task.test_type.value

    pending_task.status = 'running'
    pending_task.save()
    test_environment = FileSystemManager(run_id)

    if test_type == "unittest":
        data = prepare_unittest(pending_task, language, test_environment)
        run_test.delay(run_id, data, test_environment.get_absolute_path_to())

    if test_type == "output_checking":
        tests, data, path_to_in_out_files = prepare_output_checking_environment(pending_task, language, test_environment)
        for test_number in tests:
            test_dir = prepare_output_test(run_id, data, test_number, test_environment, path_to_in_out_files)
            run_test.apply_async((pending_task.id,
                                  test_number,
                                  test_environment.get_absolute_path_to(test_dir)),
                                 countdown=1)
    clean_up_test_env.apply_async((pending_task.id, test_environment.get_absolute_path_to()), countdown=2)
