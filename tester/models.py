from django.db import models
from model_utils.fields import StatusField
from model_utils import Choices


class Language(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Problem(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()

    def __str__(self):
        return self.name


# Unique together language, id
class ProblemTest(models.Model):
    problem = models.ForeignKey(Problem)
    language = models.ForeignKey(Language)
    code = models.TextField()
    extra_description = models.TextField()

    def __str__(self):
        return "{}/{}".format(self.problem, self.language)


class TestRun(models.Model):
    STATUS = Choices('pending', 'running', 'done')

    code = models.TextField()
    problem_test = models.ForeignKey(ProblemTest)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    status = StatusField(db_index=True)

    def __str__(self):
        return "[{}:{}] for {} at {}]"\
                .format(self.id, self.status,
                        self.problem_test, self.created_at)


class RunResult(models.Model):
    STATUS = Choices('ok', 'not_ok')

    run = models.ForeignKey(TestRun)
    status = StatusField()
    output = models.TextField()
