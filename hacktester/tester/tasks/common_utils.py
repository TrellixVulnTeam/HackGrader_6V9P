import tarfile
import tempfile
import base64
import shutil
import os

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

            # Copy test file from temp_dir in test file in path_to_extract
            shutil.copyfile(os.path.join(temp_dir, test_file_name),
                            os.path.join(path_to_extract, test_file_name))

            # Get data from test requirements.txt file (the one from temp_dir)
            with open(os.path.join(temp_dir, "requirements.txt"), "r") as test_req_file:
                data = test_req_file.read()

            data = "\n" + data

            # Append data from test requirements.txt to requirements.txt in path_to_extract
            with open(os.path.join(path_to_extract, "requirements.txt"), "a") as solution_req_file:
                solution_req_file.write(data)

    @classmethod
    def extract(cls, archive_type, path_to_archive, path_to_extract="."):
        extract_method_name = "extract_{}".format(archive_type.value)
        extract_method = getattr(cls, extract_method_name, None)
        if extract_method and hasattr(extract_method, "__call__"):
            return extract_method(path_to_archive, path_to_extract)
