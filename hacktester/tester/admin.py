from django.contrib import admin
from .models import Language, TestRun, RunResult, TestType, TestWithPlainText, TestWithBinaryFile, ArchiveType
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
    list_display = ('id', 'language', 'test_type', 'status', 'is_plain', 'is_binary')


@admin.register(TestWithPlainText)
class TestWithPlainTextAdmin(admin.ModelAdmin):
    pass


@admin.register(TestWithBinaryFile)
class TestWithBinaryFileAdmin(admin.ModelAdmin):
    pass


@admin.register(RunResult)
class RunResultAdmin(admin.ModelAdmin):
    list_display = ('run', 'status', 'output')


@admin.register(ArchiveType)
class ArchiveTypeAdmin(admin.ModelAdmin):
    pass
