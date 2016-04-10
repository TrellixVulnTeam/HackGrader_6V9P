from .models import TestRun, TestWithPlainText, TestWithBinaryFile


class TestRunFactory:
    @staticmethod
    def create_run(data, files=None):
        language = data['language']
        test_type = data['test_type']
        run = None

        if data['file_type'] == 'plain':
            run = TestWithPlainText(status='pending',
                                    language=language,
                                    test_type=test_type,
                                    solution_code=data['code'],
                                    test_code=data['test'])

        if data['file_type'] == 'binary':
            run = TestWithBinaryFile(status='pending',
                                     language=language,
                                     test_type=test_type,
                                     solution=files['code'],
                                     tests=files['test'])

        return run
