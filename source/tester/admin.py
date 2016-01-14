from django.contrib import admin
from .models import Language, TestRun, RunResult, TestType
from djcelery.models import TaskMeta


@admin.register(TaskMeta)
class TaskMetaAdmin(admin.ModelAdmin):
    list_display = ('task_id', 'status', 'result', 'date_done')
    readonly_fields = ('result',)


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    pass


@admin.register(TestType)
class TestTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(TestRun)
class TestRunAdmin(admin.ModelAdmin):
    pass


@admin.register(RunResult)
class RunResultAdmin(admin.ModelAdmin):
    list_display = ('run', 'status', 'output')