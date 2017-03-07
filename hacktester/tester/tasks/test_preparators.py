import json
import re
import os
from os.path import isfile
import shutil
import logging

from django.conf import settings

from hacktester.runner.settings import OUTPUT_CHECKING, UNITTEST, JAVA, JAVASCRIPT, PYTHON, RUBY
from .common_utils import ArchiveFileHandler
from ..models import Language
from ..exceptions import IncorrectTestFileInputError, FolderAlreadyExistsError

logger = logging.getLogger(__name__)

FILE_EXTENSIONS = {l.name: l.extension for l in Language.objects.all()}


class FileSystemManager:
    MEDIA = os.path.dirname(os.path.abspath(settings.MEDIA_ROOT))
    SANDBOX = os.path.join(str(settings.ROOT_DIR), 'sandbox/')

    def __init__(self, name, destinaton=None, ):
        self.name = str(name)
        self.__inner_folders = {}
        self._absolute_path = self._create_folder(self.name, destinaton)

    def _copy_file(self, destination_path, destination_name, file_name, source_path=None):
        if source_path is None:
            source_path = FileSystemManager.MEDIA

        if file_name.startswith('/'):    # dafaq
            file_name = file_name[1:]

        source = os.path.join(str(source_path), str(file_name))
        destination = os.path.join(str(destination_path), str(destination_name))

        logger.info(source)
        logger.info(destination)

        shutil.copyfile(source, destination)

        return destination

    def _create_file(self, destination_path, destination_name, content):
        path = os.path.join(str(destination_path), str(destination_name))

        with open(path, mode='w', encoding='utf-8') as f:
            f.write(content)

    def _create_folder(self, folder_name, destination_path=None):
        if destination_path is None:
            destination_path = FileSystemManager.SANDBOX

        folder_abs_path = os.path.join(str(destination_path), str(folder_name))
        os.mkdir(folder_abs_path)
        return folder_abs_path

    def check_if_file_exists(self, file):
        files = [f for f in os.listdir(self._absolute_path) if isfile(self.get_absolute_path_to(file=f))]
        if file in files:
            msg = "file with name:'{}' already exists in test environment. path:{}"
            logger.warning(msg.format(file, self.get_absolute_path_to()))

    def add_inner_folder(self, name, destination=None):
        if destination is None and self.__inner_folders.get(name) is None:
            self.__inner_folders[name] = FileSystemManager(name, self._absolute_path)
        elif self.__inner_folders is not None:
            msg = "A folder with name:'{}' already exists in {}"
            raise FolderAlreadyExistsError(msg.format(name, self.get_absolute_path_to()))

    def copy_file(self, name, destination_file_name, destination_folder=None, source=None):
        if destination_folder is None:
            self.check_if_file_exists(destination_file_name)
            self._copy_file(self._absolute_path, destination_file_name, name, source)
        elif destination_folder in self.__inner_folders:
            self.__inner_folders[destination_folder].copy_file(name, destination_file_name, source=source)

    def create_new_file(self, name, content, destination_folder=None):
        if destination_folder is None:
            self.check_if_file_exists(name)
            self._create_file(self._absolute_path, name, content)
        elif destination_folder in self.__inner_folders:
            self.__inner_folders[destination_folder].create_new_file(name, content, None)

    def get_absolute_path_to(self, folder=None, file=None):
        if folder is None and file is None:
            return self._absolute_path
        elif folder in self.__inner_folders:
            return self.__inner_folders[folder].get_absolute_path_to(folder=None, file=file)
        elif file is not None:
            return os.path.join(self._absolute_path, file)


class PreparatorFactory:
    @staticmethod
    def get(pending_task):
        test_type = pending_task.test_type.value

        if test_type == UNITTEST:
            if pending_task.language.name.lower() == JAVASCRIPT:
                return JavaScriptPreparator(pending_task)
            elif pending_task.language.name.lower() == PYTHON:
                return PythonPreparator(pending_task)
            elif pending_task.language.name.lower() == RUBY:
                return RubyPreparator(pending_task)
            return UnittestPreparator(pending_task)

        if test_type == OUTPUT_CHECKING:
            if pending_task.language.name.lower() == JAVA:
                return JavaOutputCheckingPreparator(pending_task)
            return OutputCheckingPreparator(pending_task)


class TestPreparator:
    test_filename = None
    test_type = None

    def __init__(self, pending_task):
        self.pending_task = pending_task
        self.test_data = self.get_data(pending_task)
        self.language = pending_task.language.name.lower()
        self.test_environment = FileSystemManager(str(pending_task.id))
        self.extension = FILE_EXTENSIONS[self.language]

    def get_solution_filename(self):
        return "solution{}".format(self.extension)

    def get_test_filename(self):
        if self.test_filename is None:
            raise NotImplementedError('You must define test_filename or get_test_filename()')

        return self.test_filename

    def get_test_type(self):
        if self.test_type is None:
            raise NotImplementedError('You must define test_type or get_test_type')

        return self.test_type

    def get_data(self, pending_task):
        data = {}

        if pending_task.extra_options is not None:
            for key, value in pending_task.extra_options.items():
                data[key] = value

        return data

    def save_solution_to_test_environment(self):
        if self.pending_task.is_plain():
            self.test_environment.create_new_file(self.get_solution_filename(),
                                                  self.pending_task.testwithplaintext.solution_code)
        if self.pending_task.is_binary():
            self.test_environment.copy_file(self.pending_task.testwithbinaryfile.solution.url,
                                            self.get_solution_filename())

    def update_test_data(self):
        self.test_data['language'] = self.language
        self.test_data['solution'] = self.get_solution_filename()
        self.test_data['tests'] = self.get_test_filename()
        self.test_data['test_type'] = self.get_test_type()

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

        self.pending_task.status = 'running'
        self.pending_task.save()

        self.update_test_data()
        self.save_solution_to_test_environment()

        run_data = {
            'run_id': self.pending_task.id,
            'input_folder': self.test_environment.get_absolute_path_to()
        }

        return [run_data]


class UnittestPreparator(TestPreparator):
    test_type = UNITTEST

    def get_test_filename(self):
        return "test{}".format(self.extension)

    def prepare(self):
        run_data = super().prepare()

        if self.pending_task.is_plain():
            self.test_environment.create_new_file(self.get_test_filename(),
                                                  self.pending_task.testwithplaintext.test_code)

        if self.pending_task.is_binary():
            self.test_environment.copy_file(self.pending_task.testwithbinaryfile.test.url,
                                            self.get_test_filename())

        self.test_environment.create_new_file('data.json', json.dumps(self.test_data))

        return run_data


class JavaScriptPreparator(UnittestPreparator):

    def prepare(self):
        run_data = super().prepare()
        project_json_data = {
            "scripts": {
                "test": "mocha --reporter tap test.js"
            }
        }

        self.test_environment.create_new_file('package.json', json.dumps(project_json_data))

        return run_data


class PythonPreparator(UnittestPreparator):

    def prepare(self):
        run_data = super().prepare()

        flake8_configuration = "[flake8]\nignore = W292\nmax-line-length = 120\ndisable-noqa = True"

        self.test_environment.create_new_file('.flake8', flake8_configuration)

        return run_data


class RubyPreparator(UnittestPreparator):

    def prepare(self):
        run_data = super().prepare()

        rubocop_configuration = '''
            AllCops:
              Exclude:
                - '**/test.rb'
            Metrics/LineLength:
              Enabled: false
            Style/TrailingBlankLines:
              Enabled: false
        '''

        self.test_environment.create_new_file('.rubocop.yml', rubocop_configuration)

        return run_data


class OutputCheckingPreparator(TestPreparator):
    test_filename = 'archive'
    test_type = OUTPUT_CHECKING
    in_out_file_directory = 'tests'

    def save_archive_to_test_environment(self):
        if self.pending_task.is_plain():
            self.test_environment.copy_file(self.pending_task.testwithplaintext.test_code.url, self.get_test_filename())

        if self.pending_task.is_binary():
            self.test_environment.copy_file(self.pending_task.testwithbinaryfile.test.url, self.get_test_filename())

    def get_archive_type(self):
        if self.pending_task.is_plain():
            return self.pending_task.testwithplaintext.tests.archivetest.archive_type
        elif self.pending_task.is_binary():
            return self.pending_task.testwithbinaryfile.test.archive_type

    def extract_archive(self):
        archive_type = self.get_archive_type()
        archive_location = self.test_environment.get_absolute_path_to(file=self.get_test_filename())
        in_out_file_location = self.test_environment.get_absolute_path_to(folder=self.in_out_file_directory)
        ArchiveFileHandler.extract(archive_type, archive_location, in_out_file_location)

    def update_pending_task_test_number(self):
        test_files = os.listdir(self.test_environment.get_absolute_path_to(self.in_out_file_directory))
        tests = self.validate_test_files(test_files)
        self.pending_task.number_of_results = len(tests)
        self.pending_task.save()

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
        self.test_environment.copy_file(name=self.get_solution_filename(),
                                        destination_file_name=self.get_solution_filename(),
                                        destination_folder=current_test_dir,
                                        source=self.test_environment.get_absolute_path_to())

    def save_in_out_files_to_current_test_dir(self, current_test_dir):
        path_to_in_out_files = self.test_environment.get_absolute_path_to(self.in_out_file_directory)
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
        self.test_environment.add_inner_folder(self.in_out_file_directory)

        self.save_archive_to_test_environment()
        self.extract_archive()

        test_files = os.listdir(self.test_environment.get_absolute_path_to(self.in_out_file_directory))
        tests = self.validate_test_files(test_files)
        self.pending_task.number_of_results = len(tests)
        self.pending_task.save()

        result = []
        for test_number in tests:
            test_dir = self.prepare_output_test(test_number)
            input_folder = self.test_environment.get_absolute_path_to(test_dir)
            result.append({"input_folder": input_folder,
                           "run_id": self.pending_task.id})
        return result

    def prepare_output_test(self, test_number):
        test_input = "{}.in".format(test_number)
        test_output = "{}.out".format(test_number)
        self.test_data["tests"] = test_input
        self.test_data["output"] = test_output

        current_test_dir = test_number

        self.test_environment.add_inner_folder(name=current_test_dir)
        self.save_solution_to_current_test_dir(current_test_dir)
        self.save_in_out_files_to_current_test_dir(current_test_dir)
        self.test_environment.create_new_file('data.json', json.dumps(self.test_data), current_test_dir)

        return current_test_dir


class JavaOutputCheckingPreparator(OutputCheckingPreparator):
    def get_solution_filename(self):
        return "{}{}".format(self.test_data['class_name'], self.extension)
