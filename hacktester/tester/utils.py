from urllib.parse import urlsplit
import tarfile

from .models import TestRun


def get_base_url(uri):
    return "{0.scheme}://{0.netloc}".format(urlsplit(uri))


def get_result_status(returncode):
    if returncode == 0:
        return 'ok'

    return 'not_ok'


def get_pending_task(run_id):
    return TestRun.objects.filter(pk=run_id).first()


class ArchiveFileHandler:
    @staticmethod
    def extract_tar_gz(path_to_archive, path_to_extract):
        with tarfile.open(name=path_to_archive, mode="r:gz") as tar:
            tar.extractall(path=path_to_extract)

    @classmethod
    def extract(cls, archive_type, path_to_archive, path_to_extract="."):
        extract_method_name = "extract_{}".format(archive_type.value)
        extract_method = getattr(cls, extract_method_name, None)
        if extract_method and hasattr(extract_method, "__call__"):
            return extract_method(path_to_archive, path_to_extract)
