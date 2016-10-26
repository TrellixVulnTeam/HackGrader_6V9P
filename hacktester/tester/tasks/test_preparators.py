import json
import re
import os
import shutil
import logging

from django.conf import settings

from .common_utils import ArchiveFileHandler, get_pending_task
from ..models import Language

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

    def _delete_folder(self, path_to_folder):
        shutil.rmtree(path_to_folder)

    def add_inner_folder(self, name, destination=None):
        # TODO add functionality to add recursively __inner_folders
        if destination is None:
            self.__inner_folders[name] = FileSystemManager(name, self._absolute_path)
        # TODO add error handling if folder with that name already exists

    def copy_file(self, name, destination_file_name, destination_folder=None, source=None):
        # TODO add functionality to for recursive file addition
        if destination_folder is None:
            self._copy_file(self._absolute_path, destination_file_name, name, source)
        elif destination_folder in self.__inner_folders:
            self.__inner_folders[destination_folder].copy_file(name, destination_file_name, source=source)
        # TODO add an else that returns/raises error message

    def create_new_file(self, name, content, destination_folder=None):
        # TODO add functionality for recursive additions
        if destination_folder is None:
            self._create_file(self._absolute_path, name, content)
        elif destination_folder in self.__inner_folders:
            self.__inner_folders[destination_folder].create_new_file(name, content, None)
        # TODO add an else that returns/raises error message

    def get_absolute_path_to(self, folder=None, file=None):
        # TODO make it recursive
        if folder is None and file is None:
            return self._absolute_path
        elif folder in self.__inner_folders:
            return self.__inner_folders[folder].get_absolute_path_to(folder=None, file=file)
        elif file is not None:
            return os.path.join(self._absolute_path, file)
        # TODO add an else that returns/raises error message


def get_data(pending_task):
    data = {}
    if pending_task.extra_options is not None:
        for key, value in pending_task.extra_options.items():
            data[key] = value
    return data


class PreparatorFactory:
    pass


class TestPreparator:
    def __init__(self, pending_task):
        self.pending_task = pending_task
        self.test_data = self.get_data(pending_task)
        self.language = pending_task.language.name.lower()
        self.test_environment = FileSystemManager(str(pending_task.id))
        self.extension = FILE_EXTENSIONS[self.language]

    @property
    def solution_file_name(self):
        return "solution{}".format(self.extension)

    def prepare(self):
        """
        This method prepares the test environment for the runner
        :return dict containing the information needed for task grade_pending_run:
                    1. "input_folder": absolute path to test folder for the docker instance
                    2. "run_id": the id of the TestRun instance

        If the subclass overrides this method, it must make sure to invoke
        the base class's method before doing anything else and it's return
        value should be returned by the overridden method.
        """

        self.pending_task.status = 'running'
        run_data = {
            "run_id": self.pending_task.id,
            "input_folder": self.test_environment.get_absolute_path_to()
        }
        return run_data

    @staticmethod
    def get_data(pending_task):
        data = {}
        if pending_task.extra_options is not None:
            for key, value in pending_task.extra_options.items():
                data[key] = value
        return data


class UnittestPreparator(TestPreparator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def test_file_name(self):
        return "tests{}".format(self.extension)

    def prepare(self):
        run_data = super().prepare()
        if self.pending_task.is_plain():
            self.test_environment.create_new_file(self.solution_file_name, self.pending_task.testwithplaintext.solution_code)
            self.test_environment.create_new_file(self.test_file_name, self.pending_task.testwithplaintext.test_code)

        if self.pending_task.is_binary():
            self.test_environment.copy_file(self.pending_task.testwithbinaryfile.solution.url, self.solution_file_name)
            self.test_environment.copy_file(self.pending_task.testwithbinaryfile.test.url, self.test_file_name)

        self.test_data['language'] = self.language
        self.test_data['solution'] = self.solution_file_name
        self.test_data['tests'] = self.test_file_name
        self.test_data['test_type'] = 'unittest'

        self.test_environment.create_new_file('data.json', json.dumps(self.test_data))

        return run_data


class OutputCheckingPreparator(TestPreparator):

    @property
    def test_file_name(self):
        return "archive"


class JavaOutputCheckingPreparator(OutputCheckingPreparator):
    @property
    def solution_file_name(self):
        return "tests{}".format


def validate_test_files(test_files):
    input_files = set()
    output_files = set()
    for file in test_files:
        match = re.match("([0-9]+)\.(in|out)", file)
        if match is not None:
            test_num = int(match.groups()[0])
            type = match.groups()[1]
            if type == "in":
                input_files.add(test_num)
            else:
                output_files.add(test_num)
        else:
            "TODO"
    if input_files != output_files:
        "TODO"

    return input_files


def prepare_output_checking_environment(pending_task, language, test_environment):
    in_out_file_directory = 'tests'
    test_environment.add_inner_folder(in_out_file_directory)
    extension = FILE_EXTENSIONS[language]

    data = get_data(pending_task)
    # TODO raise exception if data is empty dict: "class_name" and "archive_type" are mandatory

    if language == "java":
        solution = "{}{}".format(data["class_name"], extension)
    else:
        solution = "solution{}".format(extension)

    archive_name = "archive.tar.gz"

    if pending_task.is_plain():
        test_environment.create_new_file(solution, pending_task.testwithplaintext.solution_code)
        test_environment.copy_file(pending_task.testwithplaintext.test_code.url, archive_name)
        archive_type = pending_task.testwithplaintext.tests.archivetest.archive_type

    if pending_task.is_binary():
        test_environment.copy_file(solution, pending_task.testwithbinaryfile.solution.url)
        test_environment.copy_file(pending_task.testwithbinaryfile.test.url, archive_name)
        archive_type = pending_task.testwithbinaryfile.test.archive_type

    archive_location = test_environment.get_absolute_path_to(file=archive_name)
    in_out_file_location = test_environment.get_absolute_path_to(folder=in_out_file_directory)
    ArchiveFileHandler.extract(archive_type, archive_location, in_out_file_location)

    test_files = os.listdir(test_environment.get_absolute_path_to(in_out_file_directory))
    tests = validate_test_files(test_files)
    pending_task.number_of_results = len(tests)
    pending_task.save()

    data['language'] = language
    data['solution'] = solution
    data['test_type'] = 'output_checking'

    return tests, data, in_out_file_location


def prepare_output_test(data, test_number, test_environment, path_to_in_out_files):
    solution = data['solution']
    test_input = "{}.in".format(test_number)
    test_output = "{}.out".format(test_number)
    data["tests"] = test_input
    data["output"] = test_output
    current_test_dir = str(test_number)

    test_environment.add_inner_folder(name=current_test_dir)
    test_environment.copy_file(name=solution,
                               destination_file_name=solution,
                               destination_folder=current_test_dir,
                               source=test_environment.get_absolute_path_to())

    test_environment.create_new_file('data.json', json.dumps(data), current_test_dir)
    test_environment.copy_file(name=test_input,
                               destination_file_name=test_input,
                               destination_folder=current_test_dir,
                               source=path_to_in_out_files)
    test_environment.copy_file(name=test_output,
                               destination_file_name=test_output,
                               destination_folder=current_test_dir,
                               source=path_to_in_out_files)

    return current_test_dir
