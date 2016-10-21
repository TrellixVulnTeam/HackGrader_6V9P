import os
import shutil
import logging

from django.conf import settings

logger = logging.getLogger(__name__)


class FileSystemManager:
    _MEDIA = os.path.dirname(os.path.abspath(settings.MEDIA_ROOT))
    _SANDBOX = os.path.join(str(settings.ROOT_DIR), 'sandbox/')

    def __init__(self, name, destinaton=None, ):
        self.name = str(name)
        self.__inner_folders = {}
        self._absolute_path = self._create_folder(self.name, destinaton)

    def _copy_file(self, destination_path, destination_name, file_name, source_path=None):
        if source_path is None:
            source_path = FileSystemManager._MEDIA

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
            destination_path = FileSystemManager._SANDBOX

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


class TestPreparator:
    pass