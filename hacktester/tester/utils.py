from urllib.parse import urlsplit
import tarfile

from .models import TestRun


def get_run_results(run, run_results):
    if run.test_type.value == "unittest":
        result = run_results[0]
        data = {'run_status': run.status,
                'result_status': result.status,
                'run_id': run.id,
                'output': result.output,
                'returncode': result.returncode}

    elif run.test_type.value == "output_checking":
        output = []
        status = 'ok'

        for result in run_results:
            if result.output != 'OK':
                status = 'not_ok'

            output.append(result.output)

        data = {'run_status': run.status,
                'result_status': status,
                'run_id': run.id,
                'output': output,
                'returncode': 0}  # TODO

    return data


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
