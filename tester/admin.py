from django.contrib import admin
from .models import Language, Problem, ProblemTest, TestRun, RunResult
from djcelery.models import TaskMeta


@admin.register(TaskMeta)
class TaskMetaAdmin(admin.ModelAdmin):
    list_display = ('task_id', 'status', 'result', 'date_done')
    readonly_fields = ('result',)


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    pass


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    pass


@admin.register(ProblemTest)
class ProblemTestAdmin(admin.ModelAdmin):
    list_display = ('problem', 'language')


@admin.register(TestRun)
class TestRunAdmin(admin.ModelAdmin):
    pass


@admin.register(RunResult)
class RunResultAdmin(admin.ModelAdmin):
    list_display = ('run', 'status', 'output')
