from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
from django.shortcuts import render

from resume.models import Resume
from service.forms import SearchForm
from service.models import Application
from service.utils import is_employer, is_worker
from vacancy.models import Vacancy


# @login_required
# def search(request):
#     query = None
#     results = []
#     vacancy_pks = []
#     user = request.user
#
#     if 'query' in request.GET:
#         form = SearchForm(request.GET)
#         if form.is_valid():
#             query = form.cleaned_data['query']
#             search_query = SearchQuery(query)
#             if is_employer(user):
#                 search_vector = SearchVector('work_name', weight='A') + \
#                                 SearchVector('experience', weight='B') + \
#                                 SearchVector('about', weight='D')
#                 results = (
#                     Resume.objects
#                     .annotate(rank=SearchRank(search_vector, search_query))
#                     .filter(Q(work_name__icontains=query) | Q(work_name__iregex=query))
#                     .order_by('-rank'))
#             elif hasattr(user, 'resume'):
#                 search_vector = SearchVector('name', weight='A') + \
#                                 SearchVector('responsibilities', weight='B') + \
#                                 SearchVector('requirements', weight='B')
#                 results = (
#                     Vacancy.published
#                     .annotate(rank=SearchRank(search_vector, search_query))
#                     .filter(Q(name__icontains=query) | Q(name__iregex=query))
#                     .order_by('-rank'))
#                 for vacancy in results:
#                     if Application.objects.filter(resume=user.resume, vacancy=vacancy).exists():
#                         vacancy_pks.append(vacancy.pk)
#             else:
#                 results = Vacancy.published.all()
#     paginator = Paginator(results, 8)
#     page_number = request.GET.get('page', 1)
#
#     try:
#         results2 = paginator.page(page_number)
#     except EmptyPage:
#         results2 = paginator.page(paginator.num_pages)
#
#     return render(request, 'service/search.html',
#                   {'query': query,
#                    'results': results2,
#                    'vacancy_pks': vacancy_pks})


# @login_required
# def feed(request):
#     vacancy_pks = []
#     user = request.user
#     rec_vacancy = None
#     rec_resumes = None
#
#     if is_worker(user):
#         try:
#             if user.resume:
#                 work_name = user.resume.work_name
#                 rec_vacancy = (Vacancy.published
#                                .annotate(rank=SearchRank(SearchVector('name'), SearchQuery(work_name)))
#                                .filter(Q(name__icontains=work_name) | Q(name__iregex=work_name))
#                                .order_by('-rank'))[:6]
#                 if not rec_vacancy:
#                     rec_vacancy = Vacancy.published.all()[:6]
#                 for vacancy in rec_vacancy:
#                     if Application.objects.filter(resume=user.resume, vacancy=vacancy).exists():
#                         vacancy_pks.append(vacancy.pk)
#         except:
#             rec_vacancy = Vacancy.published.all()[:6]
#
#     if is_employer(user):
#         if user.vacancies.exists():
#             name = user.vacancies.last().name
#             rec_resumes = (Resume.objects
#                            .annotate(rank=SearchRank(SearchVector('work_name'), SearchQuery(name)))
#                            .filter(Q(work_name__icontains=name) | Q(work_name__iregex=name))
#                            .order_by('-rank'))[:10]
#             if not rec_resumes:
#                 rec_resumes = Resume.objects.all()[:10]
#         else:
#             rec_resumes = Resume.objects.all()[:10]
#
#     return render(request, 'base.html',
#                   {'rec_vacancy': rec_vacancy,
#                    'rec_resumes': rec_resumes,
#                    'vacancy_pks': vacancy_pks})


@login_required
def search(request):
    query = request.GET.get('query')
    results = []
    vacancy_pks = []
    user = request.user

    form = SearchForm(request.GET)
    if form.is_valid():
        search_results, vacancy_pks = perform_search(query, user)
        paginator = Paginator(search_results, 8)
        page_number = request.GET.get('page', 1)

        try:
            results = paginator.page(page_number)
        except EmptyPage:
            results = paginator.page(paginator.num_pages)

    return render(request, 'service/search.html',
                  {'query': query,
                   'results': results,
                   'vacancy_pks': vacancy_pks})


def perform_search(query, user):
    if is_employer(user):
        return search_resumes(query), []
    elif hasattr(user, 'resume'):
        results, vacancy_pks = search_vacancies(query, user)
        return results, vacancy_pks
    else:
        return Vacancy.published.all(), []


def search_resumes(query):
    search_vector = SearchVector('work_name', weight='A') + \
                    SearchVector('experience', weight='B') + \
                    SearchVector('about', weight='D')
    return (
        Resume.objects
        .annotate(rank=SearchRank(search_vector, SearchQuery(query)))
        .filter(Q(work_name__icontains=query) | Q(work_name__iregex=query))
        .order_by('-rank')
    )


def search_vacancies(query, user):
    search_vector = SearchVector('name', weight='A') + \
                    SearchVector('responsibilities', weight='B') + \
                    SearchVector('requirements', weight='B')
    results = (
        Vacancy.published
        .annotate(rank=SearchRank(search_vector, SearchQuery(query)))
        .filter(Q(name__icontains=query) | Q(name__iregex=query))
        .order_by('-rank')
    )

    vacancy_pks = [vacancy.pk for vacancy in results if Application.objects.filter(
        resume=user.resume, vacancy=vacancy).exists()]

    return results, vacancy_pks


@login_required
def feed(request):
    vacancy_pks = []
    user = request.user
    rec_vacancy = None
    rec_resumes = None

    try:
        if is_worker(user):
            work_name = user.resume.work_name
            rec_vacancy = (Vacancy.published
                           .annotate(rank=SearchRank(SearchVector('name'), SearchQuery(work_name)))
                           .filter(Q(name__icontains=work_name) | Q(name__iregex=work_name))
                           .order_by('-rank'))[:6]
            if not rec_vacancy:
                rec_vacancy = Vacancy.published.all()[:6]
            vacancy_pks.extend(vacancy.pk for vacancy in rec_vacancy if
                               Application.objects.filter(resume=user.resume, vacancy=vacancy).exists())
        else:
            if user.vacancies.exists():
                name = user.vacancies.last().name
                rec_resumes = (Resume.objects
                               .annotate(rank=SearchRank(SearchVector('work_name'), SearchQuery(name)))
                               .filter(Q(work_name__icontains=name) | Q(work_name__iregex=name))
                               .order_by('-rank'))[:6]
            if not rec_resumes:
                rec_resumes = Resume.objects.all()[:6]

    except (Vacancy.DoesNotExist, Resume.DoesNotExist):
        rec_vacancy = Vacancy.published.all()[:6]
        rec_resumes = Resume.objects.all()[:6]

    context = {
        'rec_vacancy': rec_vacancy,
        'rec_resumes': rec_resumes,
        'vacancy_pks': vacancy_pks,
    }

    return render(request, 'base.html', context)
