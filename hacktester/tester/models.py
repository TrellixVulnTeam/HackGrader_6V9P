from django.db import models
from model_utils.fields import StatusField
from model_utils import Choices
from jsonfield import JSONField


def tests_upload_path(instance, filename):
    return "tests/test_{}".format(filename)


def solutions_upload_path(instance, filename):
    return "solutions/solution_{}".format(filename)


class Language(models.Model):
    name = models.CharField(max_length=50)
    extension = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class TestType(models.Model):
    value = models.CharField(max_length=50)

    def __str__(self):
        return self.value


class Test(models.Model):
    file = models.FileField(upload_to=tests_upload_path, null=True, blank=True)
    is_archive = models.BooleanField(default=False)

    def __str__(self):
        return "{} {}".format(self.id, self.__class__.__name__)


class Solution(models.Model):
    file = models.FileField(upload_to=solutions_upload_path)
    is_archive = models.BooleanField(default=False)

    def __str__(self):
        return "{} {}".format(self.id, self.__class__.__name__)


class TestRun(models.Model):
    STATUS = Choices('pending', 'running', 'done', 'failed')

    language = models.ForeignKey(Language)
    test_type = models.ForeignKey(TestType)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    status = StatusField(db_index=True)
    extra_options = JSONField(null=True, blank=True)
    number_of_results = models.IntegerField(default=1)

    test = models.OneToOneField(Test, null=True, blank=True, related_name="test_run")

    solution = models.OneToOneField(Solution, null=True, blank=True, related_name="run")

    @property
    def test_file(self):
        return self.test.file

    def test_is_archive(self):
        self.test.is_archive = True
        self.test.save()

    @property
    def solution_file(self):
        return self.solution.file

    def solution_is_archive(self):
        self.solution.is_archive = True
        self.solution.save()

    def __str__(self):
        return "[{}:{}] for {} at {}]".format(self.id,
                                              self.status,
                                              self.language,
                                              self.created_at)


class RunResult(models.Model):
    PASSING = 'ok'
    FAILED = 'not_ok'
    STATUS = Choices(PASSING, FAILED)

    run = models.ForeignKey(TestRun)
    status = StatusField()
    output = models.TextField()
    returncode = models.IntegerField()
