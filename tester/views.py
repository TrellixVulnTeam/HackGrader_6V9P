from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest

from .models import TestRun, RunResult, Language, TestType
from .tasks import grade_pending_run

import json


def index(request):
    return render(request, 'index.html', locals())


def supported_languages(request):
    languages = [l.name for l in Language.objects.all()]
    return JsonResponse(languages, safe=False)


# { "language": "Python",
#   "type":     "unittest",
#   "problem_code": "....",
#   "problem_test": "...." }
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

    result = {"run_id": run.id}
    return JsonResponse(result)


def result(request, run_id):
    try:
        run = TestRun.objects.get(pk=run_id)
    except ObjectDoesNotExist as e:
        error = "No run with such id {}".format(run_id)
        return render(request, 'result.html', locals())

    try:
        result = RunResult.objects.get(run=run)
    except ObjectDoesNotExist as e:
        pass

    return render(request, 'result.html', locals())
