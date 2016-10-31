from urllib.parse import urlsplit
from hacktester.runner.settings import UNITTEST, OUTPUT_CHECKING
from .models import RunResult


def get_run_results(run, run_results):
    if run.test_type.value == UNITTEST:
        result = run_results[0]
        data = {'run_status': run.status,
                'result_status': result.status,
                'run_id': run.id,
                'output': result.output,
                'returncode': result.returncode}

    elif run.test_type.value == OUTPUT_CHECKING:
        output = []
        status = RunResult.PASSING

        for result in run_results:
            if result.output != 'OK':
                status = RunResult.FAILED

            output.append(result.output)

        if len(output) == 1:
            output = output[0]

        data = {'run_status': run.status,
                'result_status': status,
                'run_id': run.id,
                'output': output,
                'returncode': 0}

    return data


def get_base_url(uri):
    return "{0.scheme}://{0.netloc}".format(urlsplit(uri))
