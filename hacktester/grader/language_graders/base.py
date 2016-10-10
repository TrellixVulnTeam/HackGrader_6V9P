from settings import TIMELIMIT, TIMELIMIT_EXCEEDED_ERROR
from subprocess import CalledProcessError, TimeoutExpired

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

    def execute_unittest(self):
        """
        Hook for executing unittests
        Should return tuple containing returncode and output as result.
        Raise RunException if something fails
        """

    def execute_program(self):
        """
        Hook for executing programs for output checking tests
        Should return tuple containing returncode and output as result.
        Raise RunException if something fails
        """

    def execute(self):
        test_type = self.data['test_type']
        if test_type == 'unittest':
            return self.execute_unittest()
        elif test_type == 'output_checking':
            return self.execute_program()

        output = "{} is not supported test type".format(test_type)
        returncode = -1
        return returncode, output

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
        except Exception as e:
            returncode = -2
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
    $ java solution.jar
    and supplies input
    """

    def get_input(self):
        with open(self.tests) as f:
            input_string = f.read()

        return input_string

    def execute_program(self):
        args = {
            "command": self.__class__.COMMAND,
            "solution": self.solution
        }

        command = "{command} {solution}".format(**args)
        input_string = self.get_input()

        time_limit = self.data.get('time_limit') or TIMELIMIT

        try:
            returncode, output = run_cmd(command, time_limit, input_string=input_string)
        except CalledProcessError as e:
            output = e.output
            returncode = e.returncode

        return returncode, output


class DynamicLanguageUnittestMixin:
    """
    Executes dynamic languages like python & ruby in the following form
    $ python tests.py
    $ ruby tests.rb
    $ node tests.js
    """

    def execute_unittest(self):
        args = {
            "command": self.__class__.COMMAND,
            "tests": self.tests
        }

        command = "{command} {tests}".format(**args)

        time_limit = self.data.get('time_limit') or TIMELIMIT

        try:
            returncode, output = run_cmd(command, time_limit)
        except CalledProcessError as e:
            output = e.output
            returncode = e.returncode

        return returncode, output
