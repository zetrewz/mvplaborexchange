from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST

from resume.models import Resume


@require_POST
def add_resume_in_favorites(request, pk):
    resume = get_object_or_404(Resume, pk=pk)
    created = False

    if request.user not in resume.in_favorites.all():
        resume.in_favorites.add(request.user)
        created = True

    if created:
        return JsonResponse({'status': 'applied'})
    else:
        resume.in_favorites.remove(request.user)
        return JsonResponse({'status': 'removed'})


def check_in_favorites(request, pk):
    resume = Resume.objects.get(pk=pk)

    if request.user in resume.in_favorites.all():
        return JsonResponse({'applied': True})

    return JsonResponse({'applied': False})


@require_POST
def remove_resume_in_favorites(request, pk):
    resume = get_object_or_404(Resume, pk=pk)

    if request.user in resume.in_favorites.all():
        resume.in_favorites.remove(request.user)
        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error'})