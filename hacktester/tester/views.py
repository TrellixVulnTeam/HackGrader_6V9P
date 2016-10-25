import json
import time

from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotFound,\
        HttpResponse
from django.views.decorators.csrf import csrf_exempt

from hacktester.api_auth.decorators import require_api_authentication

from .models import TestRun, RunResult, Language, TestType, ArchiveType
from .tasks import prepare_for_grading
from .utils import get_base_url, get_run_results
from .factories import TestRunFactory, ArchiveTypeNotSuppliedError, ArchiveTypeNotSupportedError


def index(request):
    data = {
        'pending': 0,
        'running': 0,
        'graded': {
            'total': 0
        }
    }

    runs = TestRun.objects.all()

    for run in runs:
        if run.status in ['pending', 'running']:
            data[run.status] += 1

        if run.status == 'done':
            data['graded']['total'] += 1

            lang = run.language.name

            if lang not in data['graded']:
                data['graded'][lang] = 0

            data['graded'][lang] += 1

    return HttpResponse(json.dumps(data, indent=4), content_type='application/json')


def supported_languages(request):
    languages = [l.name for l in Language.objects.all()]
    return JsonResponse(languages, safe=False)


def supported_test_types(request):
    types = [t.value for t in TestType.objects.all()]
    return JsonResponse(types, safe=False)


def supported_archive_types(request):
    types = [archive.value for archive in ArchiveType.objects.all()]
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

    payload['language'] = language
    payload['test_type'] = test_type

    try:
        run = TestRunFactory.create_run(data=payload)
    except (ArchiveTypeNotSuppliedError, ArchiveTypeNotSupportedError) as e:
        msg = repr(e)
        return HttpResponseBadRequest(msg)

    run.save()
    prepare_for_grading.apply_async((run.id,), countdown=1)

    result = {"run_id": run.id}
    result_location = "{}{}"
    result_location = result_location.format(
            get_base_url(request.build_absolute_uri()),
            reverse('tester:check_result', args=(run.id, )))

    response = JsonResponse(result, status=202)
    response['Location'] = result_location

    return response


@csrf_exempt
@require_api_authentication
def check_result(request, run_id):
    try:
        run = TestRun.objects.get(pk=run_id)
        run_results = RunResult.objects.filter(run=run)

        if run.status != "done":
            run.refresh_from_db()
            response = HttpResponse(status=204)
            response['X-Run-Status'] = run.status
            return response

        data = get_run_results(run, run_results)
        return JsonResponse(data)
    except ObjectDoesNotExist as e:
        msg = "Run with id {} not found"
        msg = msg.format(run_id)
        return HttpResponseNotFound(msg)
