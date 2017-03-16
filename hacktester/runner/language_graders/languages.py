from .base import (
    BaseGrader,
    LintException,
    CompileException,
    OutputCheckingMixin,
    DynamicLanguageUnittestMixin,
    RequirementsFailedInstalling
)

from settings import (
    PYTHON, RUBY, JAVA, JAVASCRIPT,
    TIMELIMIT, JUNIT, HAMCREST,
    DEPENDENCIES_TIMELIMIT,
    DJANGO_DEPENDENCIES_FILENAME
)

import return_codes

from subprocess import CalledProcessError
from .proc import run_cmd


class PythonRunner(OutputCheckingMixin, DynamicLanguageUnittestMixin, BaseGrader):
    COMMAND = 'python3.5'
    LANGUAGE_NAME = PYTHON

    def lint(self):
        returncode, output = run_cmd("flake8 {}".format(self.solution), timeout=TIMELIMIT)
        if returncode != 0:
            raise LintException("flake8: {}".format(output))

    def install_dependencies(self):
        returncode, output = run_cmd("pip3 install -r {} --user".format(DJANGO_DEPENDENCIES_FILENAME),
                                     timeout=DEPENDENCIES_TIMELIMIT)
        if returncode != 0:
            raise RequirementsFailedInstalling(output)


class RubyRunner(OutputCheckingMixin, DynamicLanguageUnittestMixin, BaseGrader):
    COMMAND = 'ruby'
    LANGUAGE_NAME = RUBY

    def lint(self):
        returncode, output = run_cmd("rubocop", timeout=TIMELIMIT)
        if returncode != 0:
            raise LintException("rubocop: {}".format(output))


class JavaRunner(OutputCheckingMixin, BaseGrader):
    COMMAND = 'java'
    LANGUAGE_NAME = JAVA

    def execute_program(self):

        time_limit = self.options.get('time_limit') or TIMELIMIT
        returncode, output = run_cmd("javac {}".format(self.solution), time_limit)

        if returncode != 0:
            raise CompileException(output)

        self.solution = self.options.get("class_name")
        return super().execute_program()

    def execute_unittest(self):
        command = "{command} -cp {junit}:{hamcrest}:{tests}:{solution} org.junit.runner.JUnitCore {qualified_class_name}"  # flake8: noqa

        keys = {
            "command": self.COMMAND,
            "junit": JUNIT,
            "hamcrest": HAMCREST,
            "tests": self.tests,
            "solution": self.solution,
            "qualified_class_name": self.options.get('qualified_class_name')
        }

        time_limit = self.options.get('time_limit') or TIMELIMIT

        command = command.format(**keys)

        try:
            returncode, output = run_cmd(command, time_limit)
        except CalledProcessError as e:
            output = e.output
            returncode = return_codes.CALLED_PROCESS_ERROR

        return returncode, output


class JavaScriptRunner(DynamicLanguageUnittestMixin,
                       BaseGrader):
    """
    COMMAND is nodejs because this is what is running the JavaScript file
    but the command that starts mocha is npm test
    That's why we have both.
    """
    COMMAND = 'node'
    LANGUAGE_NAME = JAVASCRIPT

    def get_command_for_unittest(self):
        return 'npm test'
