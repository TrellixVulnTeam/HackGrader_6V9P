from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.http import JsonResponse

from .models import TestRun, RunResult, Language
from .tasks import grade_pending_run


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
    # run = TestRun(status='pending',
    #               problem_test=test,
    #               code=post_data['code'])
    # run.save()

    # grade_pending_run.delay(run.id)

    return redirect(reverse('tester:result', args=(run.id,)))


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
