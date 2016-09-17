import os

from .base import BaseGrader, DynamicLanguageExecuteMixin
from .proc import run_cmd
from settings import (TIMELIMIT, TIMELIMIT_EXCEEDED_ERROR,
                      JUNIT, HAMCREST)

from subprocess import (CalledProcessError, TimeoutExpired,
                        Popen, check_output,
                        STDOUT, PIPE)

from .proc import run_cmd, killall


class PythonGrader(DynamicLanguageExecuteMixin, BaseGrader):
    COMMAND = 'python3'
    LANGUAGE_NAME = 'python'


class RubyGrader(DynamicLanguageExecuteMixin, BaseGrader):
    COMMAND = 'ruby'
    LANGUAGE_NAME = 'ruby'


class JavaJarJUnitGrader(BaseGrader):
    LANGUAGE_NAME = 'java'
    COMMAND = 'java'

    def execute(self):
        command = "{command} -cp {junit}:{hamcrest}:{tests}:{solution} org.junit.runner.JUnitCore {qualified_class_name}"

        keys = {
            "command": self.COMMAND,
            "junit": JUNIT,
            "hamcrest": HAMCREST,
            "tests": self.tests,
            "solution": self.solution,
            "qualified_class_name": self.data['qualified_class_name']
        }

        command = command.format(**keys)

        try:
            returncode, output = run_cmd(command, TIMELIMIT)
        except CalledProcessError as e:
            output = e.output
            returncode = e.returncode

        return (returncode, output)
