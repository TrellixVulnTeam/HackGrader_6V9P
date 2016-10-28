import json

from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import transaction

from hacktester.tester.models import * # flake8: noqa


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.record_import_functions = {
            "tester.language": self.import_language,
            "tester.testtype": self.import_test_type,
            "tester.testrun": self.import_test_run,
            "tester.testwithplaintext": self.import_test_with_plain_text,
            "tester.testwithbinaryfile": self.import_test_with_binary_file,
            "tester.runresult": self.import_run_result
        }
        self.test_runs = {}

    def add_arguments(self, parser):
        parser.add_argument('--data_file',
                            type=str,
                            default='',
                            help='JSON file form which data should be imported')

        parser.add_argument('--flush_database',
                            type=bool,
                            default=False,
                            help='Flush database before faking?')

    def flush_database(self):
        call_command('flush')

    @staticmethod
    def import_language(record):
        print("Importing languages")
        language = Language()
        language.name = record["fields"]["name"]
        language.extension = record["fields"]["extension"]
        language.id = record["pk"]
        language.save()

    @staticmethod
    def import_test_type(record):
        print("Importing test types")
        test_type = TestType()
        test_type.value = record["fields"]["value"]
        test_type.id = record["pk"]
        test_type.save()

    def import_test_run(self, record):
        print("Importing test runs")
        self.test_runs[record["pk"]] = record["fields"]

    def import_test_with_plain_text(self, record):
        print("Importing plain text test runs")
        run = TestWithPlainText()
        test_run = self.test_runs[record["pk"]]

        run.status = test_run["status"]
        run.test_type = TestType.objects.get(pk=test_run["test_type"])
        run.extra_options = test_run["extra_options"]
        run.language = Language.objects.get(pk=test_run["language"])
        run.created_at = test_run["created_at"]

        run.solution_code = record["fields"]["solution_code"]
        run.tests = PlainUnittest.objects.create(tests=record["fields"]["test_code"])
        run.id = record["pk"]
        run.save()

    def import_test_with_binary_file(self, record):
        print("Importing binary file test runs")
        run = TestWithBinaryFile()
        test_run = self.test_runs[record["pk"]]

        run.status = test_run["status"]
        run.test_type = TestType.objects.get(pk=test_run["test_type"])
        run.extra_options = test_run["extra_options"]
        run.language = Language.objects.get(pk=test_run["language"])
        run.created_at = test_run["created_at"]

        run.solution = record["fields"]["solution"]
        run.id = record["pk"]
        run.save()
        run = TestRun.objects.get(pk=record["pk"])
        run.tests = BinaryUnittest.objects.create(tests=record["fields"]["tests"])
        run.save()

    @staticmethod
    def import_run_result(record):
        print("Importing run results")
        run_result = RunResult()
        run_result.status = record["fields"]["status"]
        run_result.returncode = record["fields"]["returncode"]
        run_result.run = TestRun.objects.get(pk=record["fields"]["run"])
        run_result.output = record["fields"]["output"]
        run_result.save()

    @transaction.atomic
    def handle(self, *args, **options):
        if options['flush_database']:
            self.flush_database()

        if options['data_file']:
            with open(options['data_file']) as data_file:
                data = json.load(data_file)

                print("Importing records")
                for record in data:
                    model = record['model']
                    import_function = self.record_import_functions.get(model)
                    if import_function:
                        import_function(record)
