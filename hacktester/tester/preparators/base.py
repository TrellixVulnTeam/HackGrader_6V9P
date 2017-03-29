import os
import re
import json
import logging

from hacktester.runner.settings import (
    UNITTEST,
    TEST_NAME,
    SOLUTION_NAME,
    OUTPUT_CHECKING,
)

from .filesystem_manager import FileSystemManager
from ..models import Language
from ..tasks.common_utils import extract
from ..exceptions import IncorrectTestFileInputError

logger = logging.getLogger(__name__)


class SandboxPreparator:
    def __init__(self, pending_task):
        self.pending_task = pending_task
        self.test_data = {}
        self.test_data['extra_options'] = self.pending_task.extra_options or {}
        self.test_environment = FileSystemManager(str(pending_task.id))

        self._extract_solution = self.test_data['extra_options'].get('archive_solution_type', False)
        self._extract_test = self.test_data['extra_options'].get('archive_test_type', False)

        self.archive_test_name = self.test_environment.get_path("archive_test.tar.gz")
        self.archive_solution_name = self.test_environment.get_path("archive_solution.tar.gz")

    def get_test(self):
        return "{}{}".format(TEST_NAME, self.get_extension())

    def get_solution(self):
        return "{}{}".format(SOLUTION_NAME, self.get_extension())

    def get_test_path(self):
        if self._extract_test:
            return self.test_environment.get_path(TEST_NAME)

        return self.test_environment.get_path(self.get_test())

    def get_solution_path(self):
        if self._extract_solution:
            return self.test_environment.get_path(SOLUTION_NAME)

        return self.test_environment.get_path(self.get_solution())

    def extract_test(self):
        dir_path = self.get_test_path()
        self.test_environment.create_folder(dir_path)

        self.test_environment.copy_file(self.pending_task.test_file.url, self.archive_test_name)

        extract(self.archive_test_name, dir_path)

    def extract_solution(self):
        dir_path = self.get_solution_path()
        self.test_environment.create_folder(dir_path)

        self.test_environment.copy_file(self.pending_task.solution_file.url, self.archive_solution_name)

        extract(self.archive_solution_name, dir_path)

    def save_test(self):
        if self._extract_test:
            self.pending_task.test_is_archive()
            self.extract_test()
        else:
            self.test_environment.copy_file(self.pending_task.test_file.url,
                                            self.get_test_path())

    def save_solution(self):
        if self._extract_solution:
            self.pending_task.solution_is_archive()
            self.extract_solution()
        else:
            self.test_environment.copy_file(self.pending_task.solution_file.url,
                                            self.get_solution_path())

    def move_solution_files_to_sandbox(self):
        """
        Move all files from solution/ except for the requirements.txt
        """
        if os.path.isdir(self.get_solution_path()):
            for f in os.listdir(self.get_solution_path()):
                if self.dependencies not in str(f):
                    file_path = os.path.join(self.get_solution_path(), f)
                    self.test_environment.move_file(file_path, self.test_environment.get_default_absolute_path())

    def move_test_file_to_sandbox(self):
        """
        Move the test file from test/ except for the requirements.txt
        """
        if os.path.isdir(self.get_test_path()):
            test_file = os.path.join(self.get_test_path(), self.get_test())
            if os.path.exists(test_file):
                self.test_environment.move_file(test_file, self.test_environment.get_default_absolute_path())

    def remove_solution_directory(self):
        if os.path.isdir(self.get_solution_path()):
            self.test_environment.remove_directory(self.get_solution_path())

    def remove_test_directory(self):
        if os.path.isdir(self.get_test_path()):
            self.test_environment.remove_directory(self.get_test_path())

    def create_requirements_file(self):
        if self.get_dependencies():
            content = self.merge_requirements_data() or ''
            self.test_environment.create_new_file(name=self.get_dependencies(), content=content)

    def prepare(self):
        self.save_solution()
        self.save_test()


class TestPreparator(SandboxPreparator):
    test_filename = None
    test_type = None
    dependencies = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.language = self.pending_task.language.name.lower()
        self.extension = self.get_extension()

    def get_extension(self):
        """
        TODO: Fix this
        """
        FILE_EXTENSIONS = {l.name: l.extension for l in Language.objects.all()}
        return FILE_EXTENSIONS[self.language]

    def get_test_type(self):
        if self.test_type is None:
            raise NotImplementedError('You must define test_type or get_test_type()')

        return self.test_type

    def get_dependencies(self):
        return self.dependencies

    def get_solution_requirements_data(self):
        solution_requirements_file = os.path.join(self.get_solution_path(), self.get_dependencies())
        solution_req_data = ''

        if os.path.exists(solution_requirements_file):
                with open(solution_requirements_file, "r") as f:
                    solution_req_data = f.readlines()

        return solution_req_data

    def get_test_requirements_data(self):
        test_requirements_file = os.path.join(self.get_test_path(), self.get_dependencies())
        test_req_data = ''

        if os.path.exists(test_requirements_file):
                with open(test_requirements_file, "r") as f:
                    test_req_data = f.readlines()

        return test_req_data

    def union_solution_and_test_directories(self):
        self.move_solution_files_to_sandbox()
        self.move_test_file_to_sandbox()
        self.remove_solution_directory()
        self.remove_test_directory()

    def merge_requirements_data(self):
        """
        Hook for placing logic for merging requirements files from
        solution/ and test/ into one file in sandbox/<id>/.
        Inheritors must call super().merge_requirements_data() to remove test/ and solution/
        directories - they are not needed any more.
        *Tip: Use get_solution_requirements_data() & get_test_requirements_data().
        """

    def update_test_data(self):
        self.test_data['language'] = self.language
        self.test_data['solution'] = self.get_solution()
        self.test_data['tests'] = self.get_test()
        self.test_data['test_type'] = self.get_test_type()
        self.test_data['dependencies'] = self.get_dependencies()

    def prepare(self):
        """
        This method prepares the test environment for the runner
        :return list containing the keyword arguments for each test
                that is going to be run with grade_pending_run.
                The keyword arguments are:
                    1. "input_folder": absolute path to test folder for the docker instance
                    2. "run_id": the id of the TestRun instance

        If the subclass overrides this method, it must make sure to invoke
        the base class's method before doing anything else and the overridden
        methods's return value should be the same format.
        """

        super().prepare()
        self.update_test_data()
        self.create_requirements_file()

        run_data = {
            'run_id': self.pending_task.id,
            'input_folder': self.test_environment.get_default_absolute_path()
        }

        return [run_data]


class UnittestPreparator(TestPreparator):
    test_type = UNITTEST

    def prepare(self):
        run_data = super().prepare()

        self.union_solution_and_test_directories()

        self.test_environment.create_new_file('data.json', json.dumps(self.test_data))

        return run_data


class OutputCheckingPreparator(TestPreparator):
    test_type = OUTPUT_CHECKING

    @staticmethod
    def validate_test_files(test_files):
        input_files = set()
        output_files = set()
        for file in test_files:
            match = re.match("([0-9]+)\.(in|out)", file)
            if match is not None:
                test_num = match.groups()[0]
                test_type = match.groups()[1]
                if test_type == "in":
                    input_files.add(test_num)
                else:
                    output_files.add(test_num)
            else:
                msg = "File with name '{}' was not expected. " +\
                      "Expected formats {number}.in where number is a positive integer"
                logger.warning(msg)
        if input_files != output_files:
            msg = "the set of input files does not match the set of output files. \n" +\
                  "input files: {} \n" +\
                  "output files: {} \n"
            raise IncorrectTestFileInputError(msg.format(input_files, output_files))

        return input_files

    def save_solution_to_current_test_dir(self, current_test_dir):
        self.test_environment.copy_file(name=self.get_solution(),
                                        destination_file_name=self.get_solution(),
                                        destination_folder=current_test_dir,
                                        source=self.test_environment.get_default_absolute_path())

    def save_dependencies_to_current_test_dir(self, current_test_dir):
        self.test_environment.copy_file(name=self.get_dependencies(),
                                        destination_file_name=self.get_dependencies(),
                                        destination_folder=current_test_dir,
                                        source=self.test_environment.get_default_absolute_path())

    def save_in_out_files_to_current_test_dir(self, current_test_dir):
        path_to_in_out_files = self.get_test_path()
        test_input = self.test_data['tests']
        test_output = self.test_data['output']

        self.test_environment.copy_file(name=test_input,
                                        destination_file_name=test_input,
                                        destination_folder=current_test_dir,
                                        source=path_to_in_out_files)

        self.test_environment.copy_file(name=test_output,
                                        destination_file_name=test_output,
                                        destination_folder=current_test_dir,
                                        source=path_to_in_out_files)

    def prepare(self):
        super().prepare()

        test_files = os.listdir(self.get_test_path())
        tests = self.validate_test_files(test_files)

        result = []
        for test_number in tests:
            test_dir = self.prepare_output_test(test_number)
            result.append({"input_folder": test_dir,
                           "run_id": self.pending_task.id})
        return result

    def prepare_output_test(self, test_number):
        test_input = "{}.in".format(test_number)
        test_output = "{}.out".format(test_number)
        self.test_data["tests"] = test_input
        self.test_data["output"] = test_output

        current_dir = self.test_environment.create_folder(folder_name=test_number,
                                                          destination_path=self.get_test_path())

        self.save_solution_to_current_test_dir(current_dir)

        if self.dependencies:
            self.save_dependencies_to_current_test_dir(current_dir)

        self.save_in_out_files_to_current_test_dir(current_dir)

        self.test_environment.create_new_file('data.json', json.dumps(self.test_data), current_dir)

        return current_dir
