from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotFound,\
        HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import TestRun, RunResult, Language, TestType
from .tasks import grade_pending_run
from api_auth.decorators import require_api_authentication

from .utils import get_base_url

import json


def index(request):
    return render(request, 'index.html', locals())


def supported_languages(request):
    languages = [l.name for l in Language.objects.all()]
    return JsonResponse(languages, safe=False)


def supported_test_types(request):
    types = [t.value for t in TestType.objects.all()]
    return JsonResponse(types, safe=False)


# { "language": "Python",
#   "test_type":     "unittest",
#   "code": "....",
#   "test": "...." }
@csrf_exempt
@require_api_authentication
def grade(request):
    payload = json.loads(request.body.decode('utf-8'))
    language = Language.objects.filter(name=payload['language']).first()

    if language is None:
        msg = "Language {} not supported. Please check GET /supported_languages"
        msg = msg.format(payload['language'])
        return HttpResponseBadRequest(msg)

    test_type = TestType.objects.filter(value=payload['test_type']).first()

    if test_type is None:
        msg = "Test type {} not supported. Please check GET /supported_test_types"
        msg = msg.format(payload['test_type'])
        return HttpResponseBadRequest(msg)

    run = TestRun(status='pending',
                  language=language,
                  test_type=test_type,
                  code=payload['code'],
                  test=payload['test'])

    run.save()

    grade_pending_run.delay(run.id)

    result = {"run_id": run.id}
    result_location = "{}{}"
    result_location = result_location.format(
            get_base_url(request.build_absolute_uri()),
            reverse('tester:check_result', args=(run.id, )))

    response = JsonResponse(result, status=202)
    response['Location'] = result_location

    return response


@csrf_exempt
def check_result(request, run_id):
    try:
        run = TestRun.objects.get(pk=run_id)
    except ObjectDoesNotExist as e:
        msg = "Run with id {} not found"
        msg = msg.format(run_id)
        return HttpResponseNotFound(msg)

    try:
        result = RunResult.objects.get(run=run)
    except ObjectDoesNotExist as e:
        run.refresh_from_db()
        response = HttpResponse(status=204)
        response['X-Run-Status'] = run.status

        return response

    data = {'run_status': run.status,
            'result_status': result.status,
            'run_id': run_id,
            'output': result.output,
            'returncode': result.returncode}
    return JsonResponse(data)
