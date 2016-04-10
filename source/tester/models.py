from django.db import models
from model_utils.fields import StatusField
from model_utils import Choices


class Language(models.Model):
    name = models.CharField(max_length=50)
    extension = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class TestType(models.Model):
    value = models.CharField(max_length=50)

    def __str__(self):
        return self.value


class TestRun(models.Model):
    STATUS = Choices('pending', 'running', 'done', 'failed')

    language = models.ForeignKey(Language)
    test_type = models.ForeignKey(TestType)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    status = StatusField(db_index=True)

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
    test_code = models.TextField()


def solution_upload_path(instance, filename):
    return "solution_{}/{}_{}".format(instance.language.name,
                                      instance.id,
                                      filename)


def tests_upload_path(instance, filename):
    return "tests_{}/{}_{}".format(instance.language.name,
                                   instance.id,
                                   filename)


class TestWithBinaryFile(TestRun):
    solution = models.FileField(upload_to=solution_upload_path)
    tests = models.FileField(upload_to=tests_upload_path)


class RunResult(models.Model):
    STATUS = Choices('ok', 'not_ok')

    run = models.ForeignKey(TestRun)
    status = StatusField()
    output = models.TextField()
    returncode = models.IntegerField()
