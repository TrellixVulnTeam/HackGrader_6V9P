from .models import ApiRequest
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt


@require_http_methods(["POST"])
@csrf_exempt
def get_req_and_resource_nonce(request):
    if request.POST:
        request_info = request.POST["request_info"]
        user_key = request.POST["user_key"]

        api_request = get_object_or_404(ApiRequest, user__key=user_key, request_info=request_info)
        nonce = api_request.nonce

        data = {
         'nonce': nonce
        }

        return JsonResponse(data, safe=False)
