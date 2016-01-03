from django.http import HttpResponseForbidden
from functools import wraps
import json


def require_api_authentication(func):
    @wraps(func)
    def _wrapped_view(request, *args, **kwargs):
        print(request.get_host())
        print(request.META.get('HTTP_AUTHENTICATION'))
        print(request.META.get('HTTP_DATE'))
        print(request.META.get('HTTP_X_API_KEY'))
        print(request.META.get('HTTP_X_NONCE_NUMBER'))
        return func(request, *args, **kwargs)

    return _wrapped_view
