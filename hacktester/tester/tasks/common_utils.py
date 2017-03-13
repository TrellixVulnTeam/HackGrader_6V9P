import tarfile
import io
import tempfile
import base64
import mimetypes
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

    @staticmethod
    def extract_tar_gz_from_bytes(byte_string, path_to_extract):
        file_like_object = io.BytesIO(byte_string.encode('ascii'))
        with tarfile.open(fileobj=file_like_object, mode="r:gz") as tar:
            tar.extractall(path=path_to_extract)

    @staticmethod
    def check_if_tarfile(byte_string):
        kkk = base64.b64decode(byte_string.encode('ascii'))
        temp = tempfile.TemporaryFile()
        temp.write(kkk)
        mime = mimetypes.guess_type(temp)
        print("MIMEEEEEEEEEE")
        print(mime)
        # try:
        #     # with tarfile.open(fileobj=sio, mode="r:gz") as tar:
        #     #     print(tar)
        #     #     return True
        # except tarfile.TarError:
        #     print(tarfile.TarError)
        #     return False

    @classmethod
    def extract(cls, archive_type, path_to_archive, path_to_extract="."):
        extract_method_name = "extract_{}".format(archive_type.value)
        extract_method = getattr(cls, extract_method_name, None)
        if extract_method and hasattr(extract_method, "__call__"):
            return extract_method(path_to_archive, path_to_extract)
