from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from service.models import Application
from vacancy.forms import VacancyCreateForm
from vacancy.models import Vacancy


# class VacancyListView(View):
#     template_name = 'vacancy/list.html'
#
#     def get(self, request):
#         vacancy_list = Vacancy.objects.filter(user=request.user)
#         paginator = Paginator(vacancy_list, 4)
#         page_number = request.GET.get('page', 1)
#
#         try:
#             vacancies = paginator.page(page_number)
#         except EmptyPage:
#             vacancies = paginator.page(paginator.num_pages)
#
#         context = {'vacancies': vacancies}
#         return render(request, self.template_name, context)


# class VacancyDetailView(View):
#     template_name = 'vacancy/detail.html'
#
#     def get(self, request, pk):
#         vacancy = get_object_or_404(Vacancy, pk=pk)
#         context = {'vacancy': vacancy}
#         return render(request, self.template_name, context)


# class VacancyCreateView(View):
#     template_name = 'vacancy/create.html'
#
#     def get(self, request):
#         context = {'form': VacancyCreateForm()}
#         return render(request, self.template_name, context)
#
#     def post(self, request):
#         form = VacancyCreateForm(request.POST)
#         if form.is_valid():
#             form.instance.user = request.user
#             form.save()
#             return redirect('vacancy:list')
#
#         context = {'form': form}
#         return render(request, self.template_name, context)


# class VacancyUpdateView(View):
#     template_name = 'vacancy/update.html'
#
#     def get(self, request, pk):
#         vacancy = get_object_or_404(Vacancy, pk=pk)
#         form = VacancyCreateForm(instance=vacancy)
#         context = {'form': form}
#
#         return render(request, self.template_name, context)
#
#     def post(self, request, pk):
#         vacancy = get_object_or_404(Vacancy, pk=pk)
#         form = VacancyCreateForm(request.POST,
#                                  instance=vacancy)
#
#         if form.is_valid():
#             form.save()
#             return redirect('vacancy:list')
#         context = {'form': form}
#
#         return render(request, self.template_name, context)


# class VacancyDeleteView(View):
#     template_name = 'vacancy/delete.html'
#
#     def get(self, request, pk):
#         vacancy = get_object_or_404(Vacancy, pk=pk)
#         context = {'vacancy': vacancy}
#
#         return render(request, self.template_name, context)
#
#     @staticmethod
#     def post(request, pk):
#         vacancy = get_object_or_404(Vacancy, pk=pk)
#         vacancy.delete()
#
#         return redirect('vacancy:list')


# class VacancyResponsesView(View):
#     template_name = 'vacancy/responses.html'
#
#     def get(self, request, pk):
#         vacancy = get_object_or_404(Vacancy, pk=pk)
#         responses = Application.objects.filter(vacancy=vacancy)
#         context = {'responses': responses}
#
#         return render(request, self.template_name, context)


# class FavoritesVacancy(View):
#     template_name = 'vacancy/favorites_vacancy.html'
#
#     def get(self, request):
#         fv_vacancy = request.user.favorites_vacancy.all()
#         vacancy_pks = [vacancy.pk for vacancy in fv_vacancy if Application.objects.filter(
#             resume=request.user.resume, vacancy=vacancy).exists()]
#         context = {
#             'fv_vacancy': fv_vacancy,
#             'vacancy_pks': vacancy_pks
#         }
#
#         return render(request, self.template_name, context)


class VacancyListView(ListView):
    model = Vacancy
    template_name = 'vacancy/list.html'
    context_object_name = 'vacancies'

    def get_queryset(self):
        return Vacancy.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vacancy_list = context['vacancies']
        paginator = Paginator(vacancy_list, 4)
        page_number = self.request.GET.get('page', 1)

        try:
            vacancies = paginator.page(page_number)
        except EmptyPage:
            vacancies = paginator.page(paginator.num_pages)

        context['vacancies'] = vacancies
        return context


class VacancyDetailView(DetailView):
    model = Vacancy
    template_name = 'vacancy/detail.html'
    context_object_name = 'vacancy'


class VacancyCreateView(CreateView):
    model = Vacancy
    form_class = VacancyCreateForm
    template_name = 'vacancy/create.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('vacancy:list')


class VacancyUpdateView(UpdateView):
    model = Vacancy
    form_class = VacancyCreateForm
    template_name = 'vacancy/update.html'

    def get_success_url(self):
        return reverse_lazy('vacancy:list')


class VacancyDeleteView(DeleteView):
    model = Vacancy
    template_name = 'vacancy/delete.html'
    success_url = reverse_lazy('vacancy:list')


class VacancyResponsesView(ListView):
    model = Application
    template_name = 'vacancy/responses.html'
    context_object_name = 'responses'

    def get_queryset(self):
        vacancy = get_object_or_404(Vacancy, pk=self.kwargs['pk'])
        return Application.objects.filter(vacancy=vacancy)


class FavoritesVacancy(ListView):
    model = Vacancy
    template_name = 'vacancy/favorites_vacancy.html'
    context_object_name = 'fv_vacancy'

    def get_queryset(self):
        return self.request.user.favorites_vacancy.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vacancy_pks = [vacancy.pk for vacancy in context['fv_vacancy'] if
                       Application.objects.filter(resume=self.request.user.resume,
                                                  vacancy=vacancy).exists()]
        context['vacancy_pks'] = vacancy_pks

        return context
