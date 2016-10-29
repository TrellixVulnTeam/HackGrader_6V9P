from .base import BaseGrader, OutputCheckingMixin, DynamicLanguageUnittestMixin, RunException
from settings import (TIMELIMIT, JUNIT, HAMCREST,
                      PYTHON, RUBY, JAVA)
import return_codes

from subprocess import CalledProcessError, call

from .proc import run_cmd


class PythonRunner(OutputCheckingMixin, DynamicLanguageUnittestMixin, BaseGrader):
    COMMAND = 'python3'
    LANGUAGE_NAME = PYTHON


class RubyRunner(OutputCheckingMixin, DynamicLanguageUnittestMixin, BaseGrader):
    COMMAND = 'ruby'
    LANGUAGE_NAME = RUBY


class JavaRunner(OutputCheckingMixin, BaseGrader):
    COMMAND = 'java'
    LANGUAGE_NAME = JAVA

    def execute_program(self):

        time_limit = self.data.get('time_limit') or TIMELIMIT
        returncode, output = run_cmd("javac {}".format(self.solution), time_limit)

        if returncode != 0:
            raise RunException(output)

        self.solution = self.data["class_name"]
        return super().execute_program()

    def execute_unittest(self):
        command = "{command} -cp {junit}:{hamcrest}:{tests}:{solution} org.junit.runner.JUnitCore {qualified_class_name}"  # flake8: noqa

        keys = {
            "command": self.COMMAND,
            "junit": JUNIT,
            "hamcrest": HAMCREST,
            "tests": self.tests,
            "solution": self.solution,
            "qualified_class_name": self.data['qualified_class_name']
        }

        time_limit = self.data.get('time_limit') or TIMELIMIT

        command = command.format(**keys)

        try:
            returncode, output = run_cmd(command, time_limit)
        except CalledProcessError as e:
            output = e.output
            returncode = return_codes.CALLED_PROCESS_ERROR

        return returncode, output
