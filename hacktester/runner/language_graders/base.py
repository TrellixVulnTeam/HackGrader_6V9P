from subprocess import CalledProcessError, TimeoutExpired

from settings import (TIMELIMIT, TIMELIMIT_EXCEEDED_ERROR,
                      OUTPUT_CHECKING, UNITTEST)

import return_codes
from exceptions import (LintException, CompileException, RunException,
                        RequirementsFailedInstalling)

from .proc import run_cmd, killall


class BaseGrader:
    def __init__(self, data):
        self.data = data
        self.solution = data['solution']
        self.tests = data['tests']
        self.run_lint = data.get('lint', True)
        self.dependecies = data.get('archive_output_type', False)

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

    def get_command_for_unittest(self):
        args = {
            "command": self.__class__.COMMAND,
            "tests": self.tests
        }

        command = "{command} {tests}".format(**args)

        return command

    def execute_unittest(self):
        """
        Hook for executing unittests
        Should return tuple containing returncode and output as result.
        Raise RunException if something fails
        """

    def get_command_for_output_checking(self):
        args = {
            "command": self.__class__.COMMAND,
            "solution": self.solution
        }
        command = "{command} {solution}".format(**args)

        return command

    def install_dependencies(self):
        pass

    def execute_program(self):
        """
        Hook for executing programs for output checking tests
        Should return tuple containing returncode and output as result.
        Raise RunException if something fails
        """

    def execute(self):
        test_type = self.data['test_type']
        if test_type == UNITTEST:
            return self.execute_unittest()
        elif test_type == OUTPUT_CHECKING:
            return self.execute_program()

        output = "{} is not supported test type".format(test_type)
        returncode = return_codes.UNSUPPORTED_TEST_TYPE
        return returncode, output

    def run(self):
        try:
            if self.dependecies:
                self.install_dependencies()

            if self.run_lint:
                self.lint()

            self.compile()

            returncode, output = self.execute()

        except LintException as e:
            returncode = return_codes.LINT_ERROR
            output = str(e)
        except CompileException as e:
            returncode = return_codes.COMPILATION_ERROR
            output = str(e)
        except RunException as e:
            returncode = return_codes.RUN_EXCEPTION
            output = str(e)
        except RequirementsFailedInstalling as e:
            returncode = return_codes.REQUIREMENTS_FAILED
            output = str(e)
        except TimeoutExpired as e:
            returncode = return_codes.TIME_LIMIT_ERROR
            output = TIMELIMIT_EXCEEDED_ERROR
        except Exception as e:
            returncode = return_codes.UNKNOWN_EXCEPTION
            output = repr(e)
        finally:
            self.clean_up()
            return returncode, output

    def clean_up(self):
        killall(self.__class__.COMMAND)


class OutputCheckingMixin:
    """
    Executes programs in the following form
    $ python solution.py
    $ ruby solution.rb
    $ node solution.js
    and supplies input
    """

    def get_input(self):
        with open(self.tests) as f:
            input_string = f.read()

        return input_string

    def get_output(self):
        with open(self.data["output"]) as f:
            output = f.read()

        return output

    def execute_program(self):
        command = self.get_command_for_output_checking()
        input_string = self.get_input()

        time_limit = self.data.get('time_limit') or TIMELIMIT

        try:
            returncode, output = run_cmd(command, time_limit, input_string=input_string)
        except CalledProcessError as e:
            output = e.output
            returncode = return_codes.CALLED_PROCESS_ERROR

        expected_output = self.get_output()
        if returncode != 0:
            returncode = return_codes.RUN_EXCEPTION
        elif output == expected_output:
            output = "ok"
            returncode = return_codes.OK
        else:
            output = "wrong answer"
            returncode = return_codes.WRONG_ANSWER

        return returncode, output


class DynamicLanguageUnittestMixin:
    """
    Executes dynamic languages like python & ruby in the following form
    $ python tests.py
    $ ruby tests.rb
    $ node tests.js
    """

    def execute_unittest(self):
        command = self.get_command_for_unittest()
        time_limit = self.data.get('time_limit') or TIMELIMIT

        try:
            returncode, output = run_cmd(command, time_limit)
        except CalledProcessError as e:
            output = e.output
            returncode = return_codes.CALLED_PROCESS_ERROR

        return returncode, output
