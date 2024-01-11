from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, ListView

from resume.forms import ResumeCreateForm
from resume.models import Resume
from service.models import Application


# class ResumeDetailView(View):
#     template_name = 'resume/detail.html'
#
#     def get(self, request, pk):
#         resume = get_object_or_404(Resume, pk=pk)
#         context = {
#             'resume': resume
#         }
#
#         return render(request, self.template_name, context)

# class ResumeCreateView(View):
#     template_name = 'resume/create.html'
#
#     def get(self, request):
#         context = {'form': ResumeCreateForm()}
#         return render(request, self.template_name, context)
#
#     def post(self, request):
#         form = ResumeCreateForm(request.POST)
#
#         if form.is_valid():
#             form.instance.user = request.user
#             form.save()
#             return redirect('resume:list')
#
#         context = {'form': form}
#         return render(request, self.template_name, context)


# class ResumeUpdateView(View):
#     template_name = 'resume/update.html'
#
#     def get(self, request, pk):
#         resume = get_object_or_404(Resume, pk=pk)
#         form = ResumeCreateForm(instance=resume)
#
#         context = {'form': form}
#         return render(request, self.template_name, context)
#
#     def post(self, request, pk):
#         resume = get_object_or_404(Resume, pk=pk)
#         form = ResumeCreateForm(request.POST,
#                                 instance=resume)
#
#         if form.is_valid():
#             form.save()
#             return redirect('resume:list')
#
#         context = {'form': form}
#         return render(request, self.template_name, context)


# class ResumeDeleteView(View):
#     template_name = 'resume/delete.html'
#
#     def get(self, request, pk):
#         resume = get_object_or_404(Resume, pk=pk)
#
#         context = {'resume': resume}
#         return render(request, self.template_name, context)
#
#     @staticmethod
#     def post(request, pk):
#         resume = get_object_or_404(Resume, pk=pk)
#         resume.delete()
#
#         return redirect('resume:create')


# class ResumeResponsesView(View):
#     template_name = 'resume/responses.html'
#
#     def get(self, request):
#         try:
#             responses = Application.objects.filter(resume=request.user.resume)
#         except:
#             responses = []
#
#         context = {'responses': responses}
#         return render(request, self.template_name, context)


# class FavoritesResume(View):
#     template_name = 'resume/favorites_resume.html'
#
#     def get(self, request):
#         fv_resume = request.user.favorites_resume.all()
#
#         context = {'fv_resume': fv_resume}
#         return render(request, self.template_name, context)
class ResumeListView(View):
    template_name = 'resume/list.html'

    def get(self, request):
        try:
            resume = Resume.objects.get(user=request.user)
            context = {'resume': resume}
            return render(request, self.template_name, context)
        except Resume.DoesNotExist:
            return redirect('resume:create')


class ResumeDetailView(DetailView):
    template_name = 'resume/detail.html'
    model = Resume
    context_object_name = 'resume'


class ResumeCreateView(CreateView):
    template_name = 'resume/create.html'
    form_class = ResumeCreateForm

    def form_valid(self, form):
        form.instance.user = self.request.user

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('resume:list')


class ResumeUpdateView(UpdateView):
    template_name = 'resume/update.html'
    model = Resume
    form_class = ResumeCreateForm

    def get_success_url(self):
        return reverse_lazy('resume:list')


class ResumeDeleteView(DeleteView):
    template_name = 'resume/delete.html'
    model = Resume

    def get_success_url(self):
        return reverse_lazy('resume:create')


class ResumeResponsesView(View):
    template_name = 'resume/responses.html'

    def get(self, request):
        responses = Application.objects.filter(resume=request.user.resume)
        context = {'responses': responses}

        return render(request, self.template_name, context)


class FavoritesResume(ListView):
    template_name = 'resume/favorites_resume.html'
    model = Resume
    context_object_name = 'fv_resume'

    def get_queryset(self):
        return self.request.user.favorites_resume.all()
