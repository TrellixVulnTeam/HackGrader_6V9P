import uuid
import base64
from django.core.files.base import ContentFile

from .models import (TestWithPlainText, TestWithBinaryFile, ArchiveTest,
                     BinaryUnittest, PlainUnittest, ArchiveType)

from .exceptions import ArchiveTypeNotSupportedError, ArchiveTypeNotSuppliedError


class TestFactory:
    @staticmethod
    def get_archive(extra_options):
        message = "For output checking 'archive_type' extra option must be supplied. " +\
                  "Please check GET /supported_archive_types"

        if extra_options:
            archive_type = extra_options.get('archive_type', None)
            if not archive_type:
                raise ArchiveTypeNotSuppliedError(message)
        else:
            raise ArchiveTypeNotSuppliedError(message)

        archive_type = ArchiveType.objects.filter(value=archive_type).first()
        if not archive_type:
            raise ArchiveTypeNotSupportedError(
                "{archive_type} not supported. Please check GET /supported_archive_types".format(archive_type)
            )

        return archive_type

    @staticmethod
    def create_test(test_type, data):

        test = None
        file_type = data['file_type']

        if test_type.value == 'output_checking':
            test_archive = base64.b64decode(data['test'])
            test_archive = ContentFile(content=test_archive, name=str(uuid.uuid4()))

            extra_options = data.get('extra_options', None)
            archive_type = TestFactory.get_archive(extra_options)

            test = ArchiveTest(tests=test_archive, archive_type=archive_type)

        elif test_type.value == 'unittest':
            if file_type == 'plain':
                test = PlainUnittest(tests=data['test'])

            elif file_type == 'binary':
                test_file = base64.b64decode(data['test'])
                test_file = ContentFile(content=test_file, name=str(uuid.uuid4()))
                test = BinaryUnittest(tests=test_file)

        return test


class TestRunFactory:
    @staticmethod
    def create_run(data, files=None):
        language = data['language']
        test_type = data['test_type']
        extra_options = data.get('extra_options', None)
        tests = TestFactory.create_test(test_type, data)
        tests.save()

        run = None
        if data['file_type'] == 'plain':
            solution = data['code']
            run = TestWithPlainText(status='pending',
                                    language=language,
                                    test_type=test_type,
                                    solution_code=solution,
                                    tests=tests,
                                    extra_options=extra_options)

        elif data['file_type'] == 'binary':
            solution = base64.b64decode(data['code'])
            solution = ContentFile(content=solution, name=str(uuid.uuid4()))

            run = TestWithBinaryFile(status='pending',
                                     language=language,
                                     test_type=test_type,
                                     solution=solution,
                                     tests=tests,
                                     extra_options=extra_options)

        return run

