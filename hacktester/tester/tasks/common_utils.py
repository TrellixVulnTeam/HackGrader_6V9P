import tarfile
import tempfile
import base64
import shutil
import os

from hacktester.runner.settings import DJANGO_DEPENDENCIES_FILENAME

from ..models import TestRun
from hacktester.tester.models import RunResult


def get_result_status(returncode):
    if returncode == 0:
        return RunResult.PASSING

    return RunResult.FAILED


def get_pending_task(run_id):
    return TestRun.objects.filter(pk=run_id).first()


class ArchiveFileHandler:
    @staticmethod
    def extract_tar_gz(path_to_archive, path_to_extract):
        with tarfile.open(name=path_to_archive, mode="r:gz") as tar:
            tar.extractall(path=path_to_extract)

    @classmethod
    def extract_tar_gz_from_bytes(cls, byte_string, path_to_extract):
        base64_archive_string = base64.b64decode(byte_string.encode('ascii'))
        with tempfile.NamedTemporaryFile() as temp:
            temp.write(base64_archive_string)
            temp.seek(0)
            cls.extract_tar_gz(temp.name, path_to_extract)

    @classmethod
    def extract_test_tar_gz_form_bytes(cls, byte_string, path_to_extract, test_file_name):
        with tempfile.TemporaryDirectory() as temp_dir:
            cls.extract_tar_gz_from_bytes(byte_string, path_to_extract=temp_dir)
            """
            Copy test file from temp_dir in test file in path_to_extract
            If path_to_extract directory already contains test_file_name is is overriden.
            """
            shutil.copyfile(os.path.join(temp_dir, test_file_name),
                            os.path.join(path_to_extract, test_file_name))

            test_requirements_file = os.path.join(temp_dir, DJANGO_DEPENDENCIES_FILENAME)
            solution_requirements_file = os.path.join(path_to_extract, DJANGO_DEPENDENCIES_FILENAME)
            test_req_data = ''
            solution_req_data = ''
            """
            Get data from test requirements.txt file (the one from temp_dir)
            if that file exists.
            """
            if os.path.exists(test_requirements_file):
                with open(test_requirements_file, "r") as f:
                    test_req_data = f.read()
            """
            Get data from solution requirements.txt file (the one from path_to_extract)
            if that file exists.
            """
            if os.path.exists(solution_requirements_file):
                with open(solution_requirements_file, "r") as f:
                    solution_req_data = f.read()

            requirements_data = solution_req_data + '\n' + test_req_data
            """
            At the end we want to have single requirements.txt file. We open solution
            requirements file in "w+" mode which means that it will be overriden if exists
            and created if does not exist.
            """
            with open(solution_requirements_file, "w+") as f:
                f.write(requirements_data)

    @classmethod
    def extract(cls, archive_type, path_to_archive, path_to_extract="."):
        extract_method_name = "extract_{}".format(archive_type.value)
        extract_method = getattr(cls, extract_method_name, None)
        if extract_method and hasattr(extract_method, "__call__"):
            return extract_method(path_to_archive, path_to_extract)
