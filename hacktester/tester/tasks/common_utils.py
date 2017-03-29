import tarfile

from ..models import TestRun
from hacktester.tester.models import RunResult


def get_result_status(returncode):
    if returncode == 0:
        return RunResult.PASSING

    return RunResult.FAILED


def get_pending_task(run_id):
    return TestRun.objects.filter(pk=run_id).first()


def extract(path_to_archive, path_to_extract):
    with tarfile.open(name=path_to_archive, mode="r:gz") as tar:
        tar.extractall(path=path_to_extract)
