from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^', include('tester.urls', namespace='tester')),
                       url(r'^', include('api_auth.urls', namespace='api_auth')),
                       )
