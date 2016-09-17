from django.conf.urls import include, url
from django.contrib import admin


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('hacktester.tester.urls', namespace='tester')),
    url(r'', include('hacktester.api_auth.urls', namespace='api_auth')),
]
