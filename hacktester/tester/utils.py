from urllib.parse import urlsplit

from hacktester.runner.settings import UNITTEST, OUTPUT_CHECKING
from hacktester.runner import return_codes

from .models import RunResult


def get_run_results(run, run_results):
    if run.test_type.value == UNITTEST:
        result = run_results[0]
        test_status = return_codes.RETURN_CODE_OUTPUT.get(result.returncode, "unknown test run error")
        data = {
            'run_status': run.status,
            'result_status': result.status,
            'run_id': run.id,
            'output': {
                "test_status": test_status,
                "test_output": result.output
            }
        }

    elif run.test_type.value == OUTPUT_CHECKING:
        output = []
        status = RunResult.PASSING

        for result in run_results:
            if result.status != RunResult.PASSING:
                status = RunResult.FAILED

            test_status = return_codes.RETURN_CODE_OUTPUT.get(result.returncode, "unknown test run error")
            test_output = {"test_status": test_status,
                           "test_output": result.output}

            output.append(test_output)

        data = {'run_status': run.status,
                'result_status': status,
                'run_id': run.id,
                'output': output}

    return data


def get_base_url(uri):
    return "{0.scheme}://{0.netloc}".format(urlsplit(uri))
