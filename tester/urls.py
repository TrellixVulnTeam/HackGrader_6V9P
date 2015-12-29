from django.conf.urls import patterns, include, url

from .views import index, grade, result, supported_languages

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^supported_languages$', supported_languages, name='supported_languages'),
    url(r'^grade$', grade, name='grade'),
    url(r'^result/(?P<run_id>[0-9]+)/$', result, name='result'),
]
