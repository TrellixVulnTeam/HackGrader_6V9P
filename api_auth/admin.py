from django.contrib import admin
from .models import ApiUser


@admin.register(ApiUser)
class ApiUserAdmin(admin.ModelAdmin):
    list_display = ('host', 'key')
    readonly_fields = ('secret', )
