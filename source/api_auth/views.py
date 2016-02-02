from .models import ApiRequest
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
@require_http_methods(["GET"])
def get_req_and_resource_nonce(request):
    request_info = request.META.get('HTTP_REQUEST_INFO')
    user_key = request.META.get('HTTP_X_USER_KEY')

    api_request = get_object_or_404(ApiRequest, user__key=user_key, request_info=request_info)
    nonce = api_request.nonce

    data = {
     'nonce': nonce
    }

    return JsonResponse(data, safe=False)
