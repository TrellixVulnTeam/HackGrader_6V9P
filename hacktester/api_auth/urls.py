from django.conf.urls import url

from .views import *  # flake8: noqa

urlpatterns = [
    url(r'^nonce$', get_req_and_resource_nonce, name='get_req_and_resource_nonce'),
]
