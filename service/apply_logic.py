from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST

from service.models import Application
from vacancy.models import Vacancy


@require_POST
def apply(request, pk):
    vacancy = get_object_or_404(Vacancy, pk=pk)
    resume = request.user.resume  # Need message, because user can be without resume
    user_application, created = Application.objects \
        .get_or_create(resume=resume, vacancy=vacancy)

    if created:
        return JsonResponse({'status': 'applied'})
    else:
        user_application.delete()
        return JsonResponse({'status': 'removed'})


def check_application(request, pk):
    try:
        vacancy = Vacancy.objects.get(pk=pk)
        resume = request.user.resume
        applied = Application.objects.filter(
            resume=resume, vacancy=vacancy).exists()
        return JsonResponse({'applied': applied})
    except Vacancy.DoesNotExist:
        return JsonResponse({'applied': False})


@require_POST
def remove_application(request, pk):
    vacancy = get_object_or_404(Vacancy, pk=pk)
    resume = request.user.resume
    application = Application.objects.filter(
        resume=resume, vacancy=vacancy).first()

    if application:
        application.delete()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error'})