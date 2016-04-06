import os
from settings import TIMELIMIT, TIMELIMIT_EXCEEDED_ERROR

import shlex
from subprocess import (CalledProcessError, TimeoutExpired,
                        Popen, check_output,
                        STDOUT, PIPE)

from .proc import run_cmd, killall


class LintException(Exception):
    pass


class CompileException(Exception):
    pass


class RunException(Exception):
    pass


class BaseGrader:
    def __init__(self, data):
        self.data = data
        self.solution = data['solution']
        self.tests = data['tests']

    def prepare(self):
        """
        Hook for setting everything up before next operations
        Use self.data to access everything passed
        """

    def lint(self):
        """
        Hook for running a linter.
        If linter fails, raise LintException with the error as message
        """

    def compile(self):
        """
        Hook for compiling the code
        If compiling fails, raise CompileException with the error as message
        """

    def execute(self):
        """
        Hook for running the code / compiled code
        Should return the output as result.
        Raise RunException if something fails
        """

    def run(self):
        try:
            self.lint()
            self.compile()
            returncode, output = self.execute()
        except LintException as e:
            returncode = 2
            output = str(e)
        except CompileException as e:
            returncode = 3
            output = str(e)
        except RunException as e:
            returncode = 4
            output = str(e)
        except TimeoutExpired as e:
            returncode = 5
            output = TIMELIMIT_EXCEEDED_ERROR
        finally:
            self.clean_up()
            return (returncode, output)

    def clean_up(self):
        killall(self.__class__.COMMAND)


class DynamicLanguageExecuteMixin:
    """
    Executes dynamic languages like python & ruby in the following form
    $ python tests.py
    $ ruby tests.rb
    $ node tests.js
    """

    def execute(self):
        args = {
            "command": self.__class__.COMMAND,
            "tests": self.tests
        }

        command = "{command} {tests}".format(**args)

        try:
            returncode, output = run_cmd(command, TIMELIMIT)
        except CalledProcessError as e:
            output = e.output
            returncode = e.returncode

        return (returncode, output)
