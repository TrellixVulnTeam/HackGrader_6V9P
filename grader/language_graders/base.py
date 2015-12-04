import os
from HackTester.settings import BASE_DIR

from subprocess import CalledProcessError, check_output, STDOUT, TimeoutExpired


class BaseGrader:
    SAVE_TO = "codespace/"

    def __init__(self, code_under_test="", tests=""):
        self.code_path = os.path.join(BASE_DIR,
                                      BaseGrader.SAVE_TO)
        self.solution_file = os.path.join(self.code_path,
                                          self.__class__.SOLUTION_FILE)
        self.tests_file = os.path.join(self.code_path,
                                       self.__class__.TESTS_FILE)

        self.write_code_under_test(code_under_test)
        self.write_tests(tests)

    def write_code_under_test(self, source):
        with open(self.solution_file, 'w') as f:
            f.write(source)

    def write_tests(self, source):
        with open(self.tests_file, 'w') as f:
            f.write(source)

    def run_code(self):
        keys = {
            "tests": self.tests_file,
            "solution": self.solution_file
        }

        command = self.__class__.COMMAND.format(**keys)
        args = self.__class__.ARGS.format(**keys)

        try:
            output = check_output([command, args],
                                  stderr=STDOUT,
                                  shell=False,
                                  timeout=2)
            returncode = 0
        except CalledProcessError as e:
            output = e.output
            returncode = e.returncode
        except TimeoutExpired as e:
            output = "Time limit exceeded. Maybe infinite loop?"
            returncode = 1
        finally:
            self.clean_up()

        return (returncode, output)

    def clean_up(self):
        os.remove(self.solution_file)
        os.remove(self.tests_file)
