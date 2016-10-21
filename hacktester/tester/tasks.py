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


class FileSystemManager:
    _MEDIA = os.path.dirname(os.path.abspath(settings.MEDIA_ROOT))
    _SANDBOX = os.path.join(str(settings.ROOT_DIR), SANDBOX)

    def __init__(self, name, destinaton=None, ):
        self.name = str(name)
        self.inner_folders = {}
        self.absolute_path = self._create_folder(self.name, destinaton)

    def _copy_file(self, destination_path, destination_name, file_name, source_path=None):
        if source_path is None:
            source_path = FileSystemManager._MEDIA

        if file_name.startswith('/'):    # dafaq
            file_name = file_name[1:]

        source = os.path.join(str(source_path), str(file_name))
        destination = os.path.join(str(destination_path), str(destination_name))

        logger.info(source)
        logger.info(destination)

        shutil.copyfile(source, destination)

        return destination

    def _create_file(self, destination_path, destination_name, content):
        path = os.path.join(str(destination_path), str(destination_name))

        with open(path, mode='w', encoding='utf-8') as f:
            f.write(content)

    def _create_folder(self, folder_name, destination_path=None):
        if destination_path is None:
            destination_path = FileSystemManager._SANDBOX

        folder_abs_path = os.path.join(str(destination_path), str(folder_name))
        os.mkdir(folder_abs_path)
        return folder_abs_path

    def _delete_folder(self, path_to_folder):
        shutil.rmtree(path_to_folder)

    def add_inner_folder(self, name, destination=None):
        # TODO add functionality to add recursively inner_folders
        if destination is None:
            self.inner_folders[name] = FileSystemManager(name, self.absolute_path)
        # TODO add error handling if folder with that name already exists

    def copy_file(self, name, destination_file_name, destination_folder=None, source=None):
        # TODO add functionality to for recursive file addition
        if destination_folder is None:
            self._copy_file(self.absolute_path, destination_file_name, name, source)
        elif destination_folder in self.inner_folders:
            self.inner_folders[destination_folder].copy_file(name, destination_file_name, source=source)
        # TODO add an else that returns/raises error message

    def create_new_file(self, name, content, destination_folder=None):
        # TODO add functionality for recursive additions
        if destination_folder is None:
            self._create_file(self.absolute_path, name, content)
        elif destination_folder in self.inner_folders:
            self.inner_folders[destination_folder].create_new_file(name, content, None)
        # TODO add an else that returns/raises error message

    def get_absolute_path_to(self, folder=None, file=None):
        # TODO make it recursive
        if folder is None and file is None:
            return self.absolute_path
        elif folder in self.inner_folders:
            return self.inner_folders[folder].get_absolute_path_to(folder=None, file=file)
        elif file is not None:
            return os.path.join(self.absolute_path, file)
        # TODO add an else that returns/raises error message

    def clean_up(self, folder=None):
        if folder is None:
            self._delete_folder(self.absolute_path)
        elif folder in self.inner_folders:
            self._delete_folder(self.inner_folders[folder])
        # TODO add an else that returns/raises error message


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
    return TestRun.objects.filter(pk=run_id).first()


def prepare_and_run_tests(task_obj, run_id):
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
        start_unittest(task_obj, data, test_environment, run_id)

    if test_type == "output_checking":
        tests, data, path_to_in_out_files = prepare_output_checking(pending_task, language, test_environment)
        for test_number in tests:
            pending_task = get_pending_task(run_id)
            solution = data['solution']
            test_input = "{}.in".format(test_number)
            test_output = "{}.out".format(test_number)
            data["tests"] = test_input
            data["output"] = test_output
            current_test_dir = str(test_number)

            test_environment.add_inner_folder(name=current_test_dir)
            test_environment.copy_file(name=solution,
                                       destination_file_name=solution,
                                       destination_folder=current_test_dir,
                                       source=test_environment.get_absolute_path_to())

            test_environment.create_new_file('data.json', json.dumps(data), current_test_dir)
            test_environment.copy_file(name=test_input,
                                       destination_file_name=test_input,
                                       destination_folder=current_test_dir,
                                       source=path_to_in_out_files)
            test_environment.copy_file(name=test_output,
                                       destination_file_name=test_output,
                                       destination_folder=current_test_dir,
                                       source=path_to_in_out_files)

            run_output_checking_test.apply_async((pending_task.id,
                                                  test_number,
                                                  test_environment.get_absolute_path_to(current_test_dir)),
                                                 countdown=1)

        clean_up_output_checking.apply_async((pending_task.id, test_environment.get_absolute_path_to()), countdown=2)


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


def start_unittest(task_obj, data, test_environment, run_id):
    status, output, returncode = run_tests(task_obj, data, input_folder=test_environment.absolute_path)
    pending_task = get_pending_task(run_id)
    test_environment.clean_up()
    pending_task.status = status
    pending_task.save()

    run_result = RunResult()
    run_result.run = pending_task
    run_result.returncode = returncode
    run_result.status = get_result_status(returncode)
    run_result.output = output
    run_result.save()
    return run_result.id


def prepare_unittest(pending_task, language, test_environment):
    extension = FILE_EXTENSIONS[language]
    solution = 'solution{}'.format(extension)
    tests = 'tests{}'.format(extension)

    if pending_task.is_plain():
        test_environment.create_new_file(solution, pending_task.testwithplaintext.solution_code)
        test_environment.create_new_file(tests, pending_task.testwithplaintext.test_code)

    if pending_task.is_binary():
        test_environment.copy_file(pending_task.testwithbinaryfile.solution.url, solution)
        test_environment.copy_file(pending_task.testwithbinaryfile.test.url, tests)

    data = {
        'language': language,
        'solution': solution,
        'tests': tests,
        'test_type': 'unittest',
    }

    if pending_task.extra_options is not None:
        for key, value in pending_task.extra_options.items():
            data[key] = value

    test_environment.create_new_file('data.json', json.dumps(data))

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


def prepare_output_checking(pending_task, language, test_environment):
    in_out_file_directory = "tests"
    test_environment.add_inner_folder(in_out_file_directory)
    extension = FILE_EXTENSIONS[language]
    solution = "solution{}".format(extension)
    archive_name = "archive.tar.gz"

    if pending_task.is_plain():
        test_environment.create_new_file(solution, pending_task.testwithplaintext.solution_code)
        test_environment.copy_file(pending_task.testwithplaintext.test_code.url, archive_name)
        archive_type = pending_task.testwithplaintext.tests.binaryarchivetest.archive_type

    if pending_task.is_binary():
        test_environment.copy_file(solution, pending_task.testwithbinaryfile.solution.url)
        test_environment.copy_file(pending_task.testwithbinaryfile.test.url, archive_name)
        archive_type = pending_task.testwithbinaryfile.test.archive_type

    archive_location = test_environment.get_absolute_path_to(file=archive_name)
    in_out_file_location = test_environment.get_absolute_path_to(folder=in_out_file_directory)
    ArchiveFileHandler.extract(archive_type, archive_location, in_out_file_location)

    test_files = os.listdir(test_environment.get_absolute_path_to(in_out_file_directory))
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
    return tests, data, in_out_file_location


@shared_task(bind=True, max_retries=settings.CELERY_TASK_MAX_RETRIES)
def run_output_checking_test(self, run_id, data, input_folder):
    pending_task = get_pending_task(run_id)
    status, output, returncode = run_tests(self,
                                           data,
                                           input_folder=input_folder)

    run_result = RunResult()
    run_result.run = pending_task
    run_result.returncode = returncode
    run_result.status = get_result_status(returncode)
    run_result.output = output
    run_result.save()

    return output, returncode


@shared_task
def clean_up_output_checking(run_id, test_folder):
    while True:
        pending_task = get_pending_task(run_id)
        results = RunResult.objects.filter(run=pending_task)
        if len(results) == pending_task.number_of_results:
            clean_up_test_env(test_folder)
            break
        time.sleep(2)


def clean_up_test_env(path_to_folder):
    shutil.rmtree(path_to_folder)


@shared_task(bind=True, max_retries=settings.CELERY_TASK_MAX_RETRIES)
def grade_pending_run(self, run_id):
    prepare_and_run_tests(self, run_id)
