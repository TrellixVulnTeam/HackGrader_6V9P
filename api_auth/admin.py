from django.contrib import admin
from .models import ApiUser, ApiRequest


@admin.register(ApiUser)
class ApiUserAdmin(admin.ModelAdmin):
    list_display = ('host', 'key')
    readonly_fields = ('secret', 'key')


@admin.register(ApiRequest)
class ApiRequestAdmin(admin.ModelAdmin):
    list_display = ('request_info', 'nonce', 'user', 'created_at')
