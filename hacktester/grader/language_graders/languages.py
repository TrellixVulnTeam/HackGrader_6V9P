from .base import BaseGrader, OutputCheckingMixin, DynamicLanguageUnittestMixin
from settings import (TIMELIMIT, TIMELIMIT_EXCEEDED_ERROR,
                      JUNIT, HAMCREST)

from subprocess import CalledProcessError

from .proc import run_cmd


class PythonRunner(OutputCheckingMixin, DynamicLanguageUnittestMixin, BaseGrader):
    COMMAND = 'python3'
    LANGUAGE_NAME = 'python'


class RubyRunner(OutputCheckingMixin, DynamicLanguageUnittestMixin, BaseGrader):
    COMMAND = 'ruby'
    LANGUAGE_NAME = 'ruby'


class JavaRunner(OutputCheckingMixin, BaseGrader):
    LANGUAGE_NAME = 'java'
    COMMAND = 'java'

    def execute_unittest(self):
        command = "{command} -cp {junit}:{hamcrest}:{tests}:{solution} org.junit.runner.JUnitCore {qualified_class_name}"

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
            returncode = e.returncode

        return returncode, output
