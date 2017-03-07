from django.conf.urls import url
from django.views.decorators.cache import cache_page
from .views import index, grade, check_result,\
    supported_languages, supported_test_types
from django.conf import settings

urlpatterns = [
    url(r'^$', cache_page(settings.CACHE_TIMEOUT)(index), name='index'),
    url(r'^supported_languages$', supported_languages, name='supported_languages'),
    url(r'^supported_test_types$', supported_test_types, name='supported_test_types'),
    url(r'^grade$', grade, name='grade'),
    url(r'^check_result/(?P<run_id>[0-9]+)/$', check_result, name='check_result'),
]
