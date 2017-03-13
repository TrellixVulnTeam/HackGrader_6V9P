import tarfile
import tempfile
import base64

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
            print(temp.read())
            cls.extract_tar_gz(temp.name, path_to_extract)

    @classmethod
    def extract(cls, archive_type, path_to_archive, path_to_extract="."):
        extract_method_name = "extract_{}".format(archive_type.value)
        extract_method = getattr(cls, extract_method_name, None)
        if extract_method and hasattr(extract_method, "__call__"):
            return extract_method(path_to_archive, path_to_extract)
