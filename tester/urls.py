from django.conf.urls import patterns, include, url

from .views import index, grade, result, supported_languages,\
    supported_test_types

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^supported_languages$', supported_languages, name='supported_languages'),
    url(r'^supported_test_types$', supported_test_types, name='supported_test_types'),
    url(r'^grade$', grade, name='grade'),
    url(r'^result/(?P<run_id>[0-9]+)/$', result, name='result'),
]
