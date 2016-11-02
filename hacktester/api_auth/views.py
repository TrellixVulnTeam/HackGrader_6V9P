from .models import ApiRequest
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Max


@csrf_exempt
@require_http_methods(["GET"])
def get_req_and_resource_nonce(request):
    request_info = request.META.get('HTTP_REQUEST_INFO')
    user_key = request.META.get('HTTP_X_USER_KEY')

    api_request = ApiRequest.objects.filter(user__key=user_key, request_info=request_info).aggregate(Max('nonce'))
    last_nonce = api_request['nonce__max']
    valid_nonce = last_nonce + 1

    data = {
     'nonce': valid_nonce
    }

    return JsonResponse(data, safe=False)
