import os
import logging
import json
from subprocess import check_output, STDOUT

from django.conf import settings


logger = logging.getLogger(__name__)


DOCKER_COMMAND = """docker run -d \
        -u {docker_user} \
        --ulimit nproc={nproc_soft_limit}:{nproc_hard_limit} \
        -m {docker_memory_limit} --memory-swap {docker_memory_limit} \
        -v {runner}:/runner -v {input}:/runner/input \
        {docker_image} \
        /bin/bash --login -c 'python3.5 runner/start.py {runner_args}'"""

DOCKER_INSPECT_COMMAND = "docker inspect -f '{state}' {container_id}"
DOCKER_LOG_COMMAND = "docker logs {container_id}"
DOCKER_CLEAR_COMMAND = "docker rm {container_id}"

CELERY_TIME_LIMIT_REACHED = """Soft time limit reached while executing \
                               language:{language}, \
                               solution:{solution}, test:{tests}"""


def prepare_docker_command(*,
                           input_folder,
                           runner=os.path.join(str(settings.APPS_DIR), "runner"),
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
    :param nproc_soft_limit: number of processes allowed to run soft limit
    :param nproc_hard_limit: number of processes allowed to run hard limit
    :param docker_memory_limit: memory limit for docker instance
    :param docker_image: docker image
    :param command_line_args: A string containing the command line arguments that
                              have to be passed to the runner
    :return: The container id used to check for the result of the runner
    """

    return DOCKER_COMMAND.format(
        **{"runner": runner,
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


def get_and_call_poll_command(container_id):
    keys = {"container_id": container_id,
            "state": "{{.State.Running}}"}
    command = DOCKER_INSPECT_COMMAND.format(**keys)

    return check_output(['/bin/bash', '-c', command],
                        stderr=STDOUT).decode('utf-8').strip()


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
