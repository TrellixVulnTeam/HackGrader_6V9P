from django.contrib import admin
from .models import ApiUser, ApiRequest


@admin.register(ApiUser)
class ApiUserAdmin(admin.ModelAdmin):
    list_display = ('host', 'key')
    readonly_fields = ('secret', )


@admin.register(ApiRequest)
class ApiRequestAdmin(admin.ModelAdmin):
    list_display = ('nonce', 'user', 'created_at')
