import json

from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotFound, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import api_view

from hacktester.api_auth.decorators import require_api_authentication

from .models import TestRun, RunResult, Language, TestType
from .tasks import prepare_for_grading
from .utils import get_base_url, get_run_results
from .factories import TestRunFactory
from .serializers import TestRunSerializer


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
    types = "tar.gz"
    return JsonResponse(types, safe=False)


# { "language": "Python",
#   "test_type":     "unittest",
#   "solution": "....",
#   "test": "...." }
@csrf_exempt
@api_view(['POST'])
@require_api_authentication
def grade(request):
    payload = json.loads(request.body.decode('utf-8'))
    serializer = TestRunSerializer(data=payload)
    if serializer.is_valid():
        run = TestRunFactory.create_run(data=dict(serializer.data))
    else:
        error_messages = []
        for _, error in serializer.errors.items():
            error_messages.append(error)

        for error_idx in range(len(error_messages)):
            error_messages[error_idx] = ", ".join(error_messages[error_idx])

        return HttpResponseBadRequest(", ".join(error_messages))
    run.save()
    prepare_for_grading.apply_async((run.id,), countdown=1)

    result = {"run_id": run.id}
    result_location = "{}{}".format(get_base_url(request.build_absolute_uri()),
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
