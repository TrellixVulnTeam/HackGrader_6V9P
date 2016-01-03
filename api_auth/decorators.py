from django.http import HttpResponseForbidden,\
        HttpResponseBadRequest
from functools import wraps
import json
import hashlib
import hmac

from .models import ApiUser
from .utils import keys_not_present

KEYS = ['HTTP_AUTHENTICATION',
        'HTTP_DATE',
        'HTTP_X_API_KEY',
        'HTTP_X_NONCE_NUMBER']


def require_api_authentication(func):
    @wraps(func)
    def _wrapped_view(request, *args, **kwargs):
        missing_headers = keys_not_present(KEYS, request.META)

        if len(missing_headers) > 0:
            msg = "The following HTTP headers are required: {}"
            msg = msg.format(', '.join(missing_headers))
            return HttpResponseBadRequest(msg)

        host = request.get_host()
        digest = request.META.get('HTTP_AUTHENTICATION')
        date = request.META.get('HTTP_DATE')
        api_key = request.META.get('HTTP_X_API_KEY')
        nonce = request.META.get('HTTP_X_NONCE_NUMBER')
        body = request.body

        api_user = ApiUser.objects.filter(key=api_key).first()

        if api_user is None:
            msg = "No API User for key {}".format(api_key)
            return HttpResponseForbidden(msg)

        msg = body.decode('utf-8') + date + nonce
        check_digest = hmac.new(bytearray(api_user.secret.encode('utf-8')),
                                msg=msg.encode('utf-8'),
                                digestmod=hashlib.sha256).hexdigest()

        if digest != check_digest:
            msg = 'None-matching digest'
            return HttpResponseForbidden(msg)

        return func(request, *args, **kwargs)

    return _wrapped_view
