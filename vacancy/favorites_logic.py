from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST

from vacancy.models import Vacancy


@require_POST
def add_vacancy_in_favorites(request, pk):
    vacancy = get_object_or_404(Vacancy, pk=pk)
    created = False

    if request.user not in vacancy.in_favorites.all():
        vacancy.in_favorites.add(request.user)
        created = True

    if created:

        return JsonResponse({'status': 'applied'})

    else:
        vacancy.in_favorites.remove(request.user)

        return JsonResponse({'status': 'removed'})


def check_vacancy_in_favorites(request, pk):
    vacancy = Vacancy.objects.get(pk=pk)

    if request.user in vacancy.in_favorites.all():

        return JsonResponse({'applied': True})

    return JsonResponse({'applied': False})


@require_POST
def remove_vacancy_in_favorites(request, pk):
    vacancy = get_object_or_404(Vacancy, pk=pk)

    if request.user in vacancy.in_favorites.all():
        vacancy.in_favorites.remove(request.user)

        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error'})
