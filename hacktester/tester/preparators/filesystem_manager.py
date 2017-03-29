import os
import shutil
import logging

from django.conf import settings

logger = logging.getLogger(__name__)


class FileSystemManager:
    MEDIA = os.path.dirname(os.path.abspath(settings.MEDIA_ROOT))
    SANDBOX = os.path.join(str(settings.ROOT_DIR), 'sandbox/')

    def __init__(self, name, destinaton=None, ):
        self.name = str(name)
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

        return path

    def _create_folder(self, folder_name, destination_path=None):
        if destination_path is None:
            destination_path = FileSystemManager.SANDBOX

        folder_abs_path = os.path.join(str(destination_path), str(folder_name))
        os.mkdir(folder_abs_path)
        return folder_abs_path

    def create_folder(self, folder_name, destination_path=None):
        if destination_path is None:
            return self._create_folder(folder_name=folder_name)

        return self._create_folder(folder_name=folder_name, destination_path=destination_path)

    def check_if_file_exists(self, file):
        files = [f for f in os.listdir(self._absolute_path) if os.path.isfile(os.path.abspath(f))]
        if file in files:
            msg = "file with name:'{}' already exists in test environment. path:{}"
            logger.warning(msg.format(file, self._absolute_path))

    def copy_file(self, name, destination_file_name, destination_folder=None, source=None):
        if destination_folder is None:
            self.check_if_file_exists(destination_file_name)
            self._copy_file(self._absolute_path, destination_file_name, name, source)
        else:
            self._copy_file(destination_folder, destination_file_name, name, source)

    def create_new_file(self, name, content, destination_folder=None):
        if destination_folder is None:
            self._create_file(self._absolute_path, name, content)
        else:
            self._create_file(destination_folder, name, content)

    def get_path(self, name):
        return os.path.join(self._absolute_path, name)

    def get_default_absolute_path(self):
        return self._absolute_path

    def move_file(self, current_path, new_path):
        if os.path.exists(current_path):
            shutil.move(current_path, new_path)

    def remove_directory(self, folder_path):
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)
