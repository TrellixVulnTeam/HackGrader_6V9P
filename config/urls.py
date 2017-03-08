from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings


urlpatterns = [
    url(settings.ADMIN_URL, include(admin.site.urls)),
    url(r'^docs/*', include('docs.urls')),
    url(r'', include('hacktester.tester.urls', namespace='tester')),
    url(r'', include('hacktester.api_auth.urls', namespace='api_auth')),
]
