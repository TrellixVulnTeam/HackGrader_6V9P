from django.contrib import admin
from .models import Language, TestRun, RunResult, TestType


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    pass


@admin.register(TestType)
class TestTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(TestRun)
class TestRunAdmin(admin.ModelAdmin):
    list_display = ('id', 'language', 'test_type', 'status')


@admin.register(RunResult)
class RunResultAdmin(admin.ModelAdmin):
    list_display = ('run', 'status', 'output')
