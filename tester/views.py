from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.http import JsonResponse

from .models import Problem, ProblemTest, TestRun, RunResult, Language
from .tasks import grade_pending_run


def index(request):
    problem_id = request.GET.get('problem')

    if problem_id is not None:
        selected_problem = Problem.objects.get(pk=problem_id)
    else:
        selected_problem = Problem.objects.first()

    problems = Problem.objects.filter(problemtest__isnull=False).distinct()
    problems = [p for p in problems if p != selected_problem]

    tests = ProblemTest.objects.filter(problem=selected_problem)

    return render(request, 'index.html', locals())


def supported_languages(request):
    languages = [l.name for l in Language.objects.all()]
    return JsonResponse(languages, safe=False)


def grade(request):
    post_data = request.POST
    test = ProblemTest.objects.get(pk=request.POST.get('test'))
    run = TestRun(status='pending',
                  problem_test=test,
                  code=post_data['code'])
    run.save()

    grade_pending_run.delay(run.id)

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
