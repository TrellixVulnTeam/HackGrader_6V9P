import uuid
import base64
from django.core.files.base import ContentFile

from .models import TestRun, TestWithPlainText, TestWithBinaryFile


class TestRunFactory:
    @staticmethod
    def create_run(data, files=None):
        language = data['language']
        test_type = data['test_type']
        extra_options = data.get('extra_options', None)

        run = None

        if data['file_type'] == 'plain':
            run = TestWithPlainText(status='pending',
                                    language=language,
                                    test_type=test_type,
                                    solution_code=data['code'],
                                    test_code=data['test'],
                                    extra_options=extra_options)

        if data['file_type'] == 'binary':
            solution = base64.b64decode(data['code'])
            solution = ContentFile(content=solution,
                                   name=str(uuid.uuid4()))

            tests = base64.b64decode(data['test'])
            tests = ContentFile(content=tests,
                                name=str(uuid.uuid4()))

            run = TestWithBinaryFile(status='pending',
                                     language=language,
                                     test_type=test_type,
                                     solution=solution,
                                     tests=tests,
                                     extra_options=extra_options)

        return run
