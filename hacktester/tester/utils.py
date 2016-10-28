from urllib.parse import urlsplit
from hacktester.runner.settings import UNITTEST, OUTPUT_CHECKING


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
        status = 'ok'

        for result in run_results:
            if result.output != 'OK':
                status = 'not_ok'

            output.append(result.output)

        if len(output) == 1:
            output = output[1]

        data = {'run_status': run.status,
                'result_status': status,
                'run_id': run.id,
                'output': output,
                'returncode': 0}  # TODO

    return data


def get_base_url(uri):
    return "{0.scheme}://{0.netloc}".format(urlsplit(uri))
