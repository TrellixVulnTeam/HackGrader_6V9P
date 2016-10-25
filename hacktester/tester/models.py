from django.db import models
from model_utils.fields import StatusField
from model_utils import Choices
from jsonfield import JSONField


class Language(models.Model):
    name = models.CharField(max_length=50)
    extension = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class TestType(models.Model):
    value = models.CharField(max_length=50)

    def __str__(self):
        return self.value


class ArchiveType(models.Model):
    value = models.CharField(max_length=50)

    def __str__(self):
        return self.value


class Test(models.Model):
    def __str__(self):
        return "{} {}".format(self.id, self.__class__.__name__)


def tests_upload_path(instance, filename):
    return "tests_{}_{}_{}".format(instance.__class__.__name__, instance.id, filename)


class BinaryUnittest(Test):
    """
    Unittest received in binary format
    example: jar files for Java
    """
    tests = models.FileField(upload_to=tests_upload_path)


class PlainUnittest(Test):
    """
    Unittest received in plain text format
    example: .py, .rb files
    """
    tests = models.TextField()


class ArchiveTest(Test):
    """
    Test received as archive file
    For output checking
    """
    tests = models.FileField(upload_to=tests_upload_path)
    archive_type = models.ForeignKey(ArchiveType)


class TestRun(models.Model):
    STATUS = Choices('pending', 'running', 'done', 'failed')

    language = models.ForeignKey(Language)
    test_type = models.ForeignKey(TestType)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    status = StatusField(db_index=True)
    extra_options = JSONField(null=True, blank=True)
    number_of_results = models.IntegerField(default=1)
    tests = models.OneToOneField(Test, null=True, blank=True, related_name="test_run")

    def is_plain(self):
        return hasattr(self, "testwithplaintext")

    def is_binary(self):
        return hasattr(self, "testwithbinaryfile")

    def __str__(self):
        return "[{}:{}] for {} at {}]"\
                .format(self.id, self.status,
                        self.language, self.created_at)


class TestWithPlainText(TestRun):
    solution_code = models.TextField()

    @property
    def test_code(self):
        if self.test_type.value == "unittest":
            return self.tests.plainunittest.tests
        if self.test_type.value == "output_checking":
            return self.tests.archivetest.tests


def solution_upload_path(instance, filename):
    return "solution_{}/{}_{}".format(instance.language.name,
                                      instance.id,
                                      filename)


class TestWithBinaryFile(TestRun):
    solution = models.FileField(upload_to=solution_upload_path)

    @property
    def test(self):
        if self.test_type.value == "unittest":
            return self.tests.binaryunittest.tests
        if self.test_type.value == "output_checking":
            return self.tests.archivetest.tests


class RunResult(models.Model):
    STATUS = Choices('ok', 'not_ok')

    run = models.ForeignKey(TestRun)
    status = StatusField()
    output = models.TextField()
    returncode = models.IntegerField()
