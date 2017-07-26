from django.contrib import admin
from .models import ApiUser, ApiRequest


@admin.register(ApiUser)
class ApiUserAdmin(admin.ModelAdmin):
    list_display = ('host', 'key')
    readonly_fields = ('key', 'secret')

    def save_model(self, request, obj, form, change):
        obj = ApiUser.create_api_user(form.cleaned_data.get('host'))
        obj.save()


@admin.register(ApiRequest)
class ApiRequestAdmin(admin.ModelAdmin):
    list_display = ('request_info', 'nonce', 'user', 'created_at')
