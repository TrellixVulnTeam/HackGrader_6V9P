from __future__ import absolute_import
import re
import os
import json
import time
import shutil
from subprocess import CalledProcessError, check_output, STDOUT, TimeoutExpired

from celery import shared_task
from celery.utils.log import get_task_logger
from celery.exceptions import SoftTimeLimitExceeded

from django.conf import settings

from .models import TestRun, RunResult, Language
from .utils import ArchiveFileHandler


logger = get_task_logger(__name__)

FILE_EXTENSIONS = {l.name: l.extension for l in Language.objects.all()}

SANDBOX = 'sandbox/'
DOCKER_COMMAND = """docker run -d \
        -u {docker_user} \
        --ulimit nproc={nproc_soft_limit}:{nproc_hard_limit} \
        -m {docker_memory_limit} --memory-swap -1 \
        --net=none \
        -v {grader}:/grader -v {input}:/grader/input \
        {docker_image} \
        /bin/bash --login -c 'python3 grader/start.py {runner_args}'"""

DOCKER_INSPECT_COMMAND = "docker inspect -f '{state}' {container_id}"
DOCKER_LOG_COMMAND = "docker logs {container_id}"
DOCKER_CLEAR_COMMAND = "docker rm {container_id}"


CELERY_TIME_LIMIT_REACHED = """Soft time limit reached while executing \
                               language:{language}, \
                               solution:{solution}, test:{tests}"""


def move_file(where, what, path):
    media = os.path.dirname(os.path.abspath(settings.MEDIA_ROOT))

    if what.startswith('/'):
        what = what[1:]

    src = os.path.join(media, what)

    dest = os.path.join(path, where)
    logger.info(src)
    logger.info(dest)

    shutil.copyfile(src, dest)
    return dest


def prepare_docker_command(*,
                           input_folder,
                           runner=os.path.join(str(settings.APPS_DIR), "grader"),
                           docker_user=settings.DOCKER_USER,
                           nproc_soft_limit=settings.NPROC_SOFT_LIMIT,
                           nproc_hard_limit=settings.NPROC_HARD_LIMIT,
                           docker_memory_limit=settings.DOCKER_MEMORY_LIMIT,
                           docker_image=settings.DOCKER_IMAGE,
                           command_line_args=None):
    """
    :param input_folder: The folder containing the tests, solution, and meta data
                         that is being passed to the docker instance
    :param runner: the runner app containing the code of the test runner
    :param docker_user: docker user
    :param nproc_soft_limit: TODO add descr
    :param nproc_hard_limit: TODO add descr
    :param docker_memory_limit: TODO add descr
    :param docker_image: docker image
    :param command_line_args: A string containing the command line arguments that
                              have to be passed to the runner
    :return: The container id used to check for the result of the runner
    """

    return DOCKER_COMMAND.format(
        **{"grader": runner,
           "input": input_folder,
           "docker_user": docker_user,
           "nproc_soft_limit": nproc_soft_limit,
           "nproc_hard_limit": nproc_hard_limit,
           "docker_memory_limit": docker_memory_limit,
           "docker_image": docker_image,
           "runner_args": command_line_args})


def save_input(where, contents, path):
    path = os.path.join(str(path), where)

    with open(path, mode='w', encoding='utf-8') as f:
        f.write(contents)


def get_output(logs):
    decoded_output = json.loads(logs)
    returncode = decoded_output["returncode"]
    output = decoded_output["output"]

    return returncode, output


def wait_while_docker_finishes(container_id):
    keys = {"container_id": container_id,
            "state": "{{.State.Running}}"}
    command = DOCKER_INSPECT_COMMAND.format(**keys)

    while True:
        result = check_output(['/bin/bash', '-c', command],
                              stderr=STDOUT).decode('utf-8').strip()

        logger.info("Checking if {} has finished: {}".format(container_id, result))
        if result == 'false':
            break

        time.sleep(1)


def run_code_in_docker(time_limit=None, **kwargs):

    time_limit = time_limit or settings.DOCKER_TIME_LIMIT
    docker_command = prepare_docker_command(**kwargs)
    return check_output(['/bin/bash', '-c', docker_command],
                        stderr=STDOUT,
                        timeout=time_limit).decode('utf-8')


def get_docker_logs(container_id):
    command = DOCKER_LOG_COMMAND.format(**{"container_id": container_id})
    logger.info(command)

    return check_output(['/bin/bash', '-c', command],
                        stderr=STDOUT).decode('utf-8')


def docker_cleanup(container_id):
    keys = {"container_id": container_id}
    command = DOCKER_CLEAR_COMMAND.format(**keys)
    check_output(['/bin/bash', '-c', command],
                 stderr=STDOUT)


def get_result_status(returncode):
    if returncode == 0:
        return 'ok'

    return 'not_ok'


def get_pending_task(run_id):
    if run_id is None:
        pending_task = TestRun.objects.filter(status='pending') \
            .order_by('-created_at') \
            .first()
    else:
        pending_task = TestRun.objects.filter(pk=run_id).first()
    return pending_task


def prepare_adn_run_tests(task_obj, run_id):
    pending_task = get_pending_task(run_id)
    if pending_task is None:
        return "No tasks to run right now."

    language = pending_task.language.name.lower()
    test_type = pending_task.test_type.value

    pending_task.status = 'running'
    pending_task.save()

    path_to_test_folder = os.path.join(str(settings.ROOT_DIR), SANDBOX, str(pending_task.id))
    os.mkdir(path_to_test_folder)

    if test_type == "unittest":
        data = prepare_unittest(pending_task, language, path_to_test_folder)
        start_unittest(task_obj, data, path_to_test_folder, run_id)

    if test_type == "output_checking":
        tests, data, path_to_in_out_files = prepare_output_checking(pending_task, language, path_to_test_folder)
        for test_number in tests:
            run_output_checking_test.apply_async((pending_task.id,
                                                  test_number,
                                                  path_to_test_folder,
                                                  path_to_in_out_files, data),
                                                 countdown=1)

        clean_up_output_checking.apply_async((pending_task.id, path_to_test_folder), countdown=2)


def run_tests(task_obj, data, **kwargs_for_docker_command):
    container_id = None
    try:
        container_id = run_code_in_docker(**kwargs_for_docker_command)
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
        task_obj.retry(exc=exc)
    finally:
        if container_id:
            docker_cleanup(container_id)

    return status, output, returncode


def start_unittest(task_obj, data, path_to_test_folder, run_id):
    status, output, returncode = run_tests(task_obj, data, input_folder=path_to_test_folder)
    pending_task = get_pending_task(run_id)
    clean_up_test_env(path_to_test_folder)
    pending_task.status = status
    pending_task.save()

    run_result = RunResult()
    run_result.run = pending_task
    run_result.returncode = returncode
    run_result.status = get_result_status(returncode)
    run_result.output = output
    run_result.save()
    return run_result.id


def prepare_unittest(pending_task, language, path_to_test_folder):
    extension = FILE_EXTENSIONS[language]
    solution = 'solution{}'.format(extension)
    tests = 'tests{}'.format(extension)

    if pending_task.is_plain():
        save_input(solution, pending_task.testwithplaintext.solution_code, path_to_test_folder)
        save_input(tests, pending_task.testwithplaintext.test_code, path_to_test_folder)

    if pending_task.is_binary():
        move_file(solution, pending_task.testwithbinaryfile.solution.url, path_to_test_folder)
        move_file(tests, pending_task.testwithbinaryfile.test.url, path_to_test_folder)

    data = {
        'language': language,
        'solution': solution,
        'tests': tests,
        'test_type': 'unittest',
    }

    if pending_task.extra_options is not None:
        for key, value in pending_task.extra_options.items():
            data[key] = value

    save_input('data.json', json.dumps(data), path_to_test_folder)

    return data


def validate_test_files(test_files):
    input_files = set()
    output_files = set()
    for file in test_files:
        match = re.match("([0-9]+)\.(in|out)", file)
        if match is not None:
            test_num = int(match.groups()[0])
            type = match.groups()[1]
            if type == "in":
                input_files.add(test_num)
            else:
                output_files.add(test_num)
        else:
            "TODO"
    if input_files != output_files:
        "TODO"

    return input_files


def prepare_output_checking(pending_task, language, path_to_test_folder):
    path_to_in_out_files = os.path.join(path_to_test_folder, "tests")
    os.mkdir(path_to_in_out_files)
    extension = FILE_EXTENSIONS[language]
    solution = 'solution{}'.format(extension)

    if pending_task.is_plain():
        save_input(solution, pending_task.testwithplaintext.solution_code, path_to_test_folder)
        test_location = move_file("archive.tar.gz", pending_task.testwithplaintext.test_code.url, path_to_test_folder)
        archive_type = pending_task.testwithplaintext.tests.binaryarchivetest.archive_type

    if pending_task.is_binary():
        move_file(solution, pending_task.testwithbinaryfile.solution.url, path_to_test_folder)
        test_location = move_file("archive.tar.gz", pending_task.testwithbinaryfile.test.url, path_to_test_folder)
        archive_type = pending_task.testwithbinaryfile.test.archive_type

    ArchiveFileHandler.extract(archive_type, test_location, path_to_in_out_files)

    test_files = os.listdir(path_to_in_out_files)
    tests = validate_test_files(test_files)
    pending_task.number_of_results = len(tests)
    pending_task.save()

    data = {
        'language': language,
        'solution': solution,
        'test_type': 'output_checking'
    }

    if pending_task.extra_options is not None:
        for key, value in pending_task.extra_options.items():
            data[key] = value
    return tests, data, path_to_in_out_files


@shared_task(bind=True, max_retries=settings.CELERY_TASK_MAX_RETRIES)
def run_output_checking_test(self, run_id, test_number, path_to_folder, path_to_in_out_files, data):
    pending_task = get_pending_task(run_id)
    solution = os.path.join(path_to_folder, data['solution'])
    current_test_directory = os.path.join(path_to_folder, str(test_number))
    os.mkdir(current_test_directory)
    solution_dest = os.path.join(str(current_test_directory), data["solution"])
    test_name = "{}.in".format(test_number)
    data["tests"] = test_name
    save_input('data.json', json.dumps(data), path=current_test_directory)
    test_location = os.path.join(path_to_in_out_files, test_name)
    test_dest = os.path.join(current_test_directory, test_name)
    shutil.copyfile(solution, solution_dest)
    shutil.copyfile(test_location, test_dest)
    status, output, returncode = run_tests(self, data, input_folder=current_test_directory, command_line_args=test_number)

    output_file = os.path.join(path_to_in_out_files, "{}.out".format(test_number))
    with open(output_file) as f:
        expected_output = f.read()

    if expected_output == output:
        output = "OK"
    else:
        output = "NOT OK"

    run_result = RunResult()
    run_result.run = pending_task
    run_result.returncode = returncode
    run_result.status = get_result_status(returncode)
    run_result.output = output
    run_result.save()
    clean_up_test_env(current_test_directory)

    return output, returncode


@shared_task
def clean_up_output_checking(run_id, path_to_test_folder):
    while True:
        pending_task = get_pending_task(run_id)
        results = RunResult.objects.filter(run=pending_task)
        if len(results) == pending_task.number_of_results:
            clean_up_test_env(path_to_test_folder)
            break
        time.sleep(2)


def clean_up_test_env(path_to_folder):
    shutil.rmtree(path_to_folder)


@shared_task(bind=True, max_retries=settings.CELERY_TASK_MAX_RETRIES)
def grade_pending_run(self, run_id):
    prepare_adn_run_tests(self, run_id)
