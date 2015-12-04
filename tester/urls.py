from django.conf.urls import patterns, include, url

from .views import index, grade, result

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^grade$', grade, name='grade'),
    url(r'^result/(?P<run_id>[0-9]+)/$', result, name='result'),
]
