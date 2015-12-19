import os
from settings import TIMELIMIT, TIMELIMIT_EXCEEDED_ERROR

from subprocess import CalledProcessError, check_output, STDOUT, TimeoutExpired


class BaseGrader:
    def __init__(self, solution, tests):
        self.solution = solution
        self.tests = tests

    def run_code(self):
        keys = {
            "tests": self.tests,
            "solution": self.solution
        }

        command = self.__class__.COMMAND.format(**keys)
        args = self.__class__.ARGS.format(**keys)

        try:
            output = check_output([command, args],
                                  stderr=STDOUT,
                                  shell=False,
                                  timeout=TIMELIMIT).decode('utf-8')
            returncode = 0
        except CalledProcessError as e:
            output = e.output.decode('utf-8')
            returncode = e.returncode
        except TimeoutExpired as e:
            output = TIMELIMIT_EXCEEDED_ERROR
            returncode = 1
        finally:
            self.clean_up()

        return (returncode, output)

    def clean_up(self):
        pass
