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

    code = models.TextField()
    test = models.TextField()
    language = models.ForeignKey(Language)
    test_type = models.ForeignKey(TestType)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    status = StatusField(db_index=True)

    def __str__(self):
        return "[{}:{}] for {} at {}]"\
                .format(self.id, self.status,
                        self.language, self.created_at)


class RunResult(models.Model):
    STATUS = Choices('ok', 'not_ok')

    run = models.ForeignKey(TestRun)
    status = StatusField()
    output = models.TextField()
    returncode = models.IntegerField()
