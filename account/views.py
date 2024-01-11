from django.contrib import messages
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.views.generic import FormView

from account.forms import UserRegistrationForm, UserLoginForm, ProfileEditForm
from account.models import EmployerProfile
from account.utils import send_email_for_verify

User = get_user_model()


# class Register(View):
#     template_name = 'registration/register.html'
#
#     def get(self, request):
#         context = {
#             'form': UserRegistrationForm()
#         }
#         return render(request, self.template_name, context)
#
#     def post(self, request):
#         form = UserRegistrationForm(request.POST)
#
#         if form.is_valid():
#             email = form.cleaned_data['email']
#             if User.objects.filter(email=email).exists():
#                 messages.error(request, 'Такой Email уже существует')
#             else:
#                 user = form.save(commit=False)
#                 user.username = email
#                 user.save()
#                 user_type = form.cleaned_data['user_type']
#                 if user_type == 'E':
#                     EmployerProfile.objects.create(user=user)
#                 send_email_for_verify(request, user)
#                 return redirect('account:confirm_email')
#         context = {
#             'form': form
#         }
#         return render(request, self.template_name, context)


# class Login(View):
#     template_name = 'registration/login.html'
#
#     def get(self, request):
#         context = {
#             'form': UserLoginForm()
#         }
#         return render(request, self.template_name, context)
#
#     def post(self, request):
#         form = UserLoginForm(request.POST)
#
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(request,
#                                 username=cd['email'],
#                                 password=cd['password'])
#             if user is not None:
#                 if user.is_active:
#                     if user.email_verify:
#                         login(request, user)
#                         return redirect('service:feed')
#                     else:
#                         send_email_for_verify(request, user)
#                         return redirect('account:confirm_email')
#                 else:
#                     messages.error(request, 'Account is disabled')
#             else:
#                 messages.error(request, 'Invalid email or password')
#         context = {
#             'form': form
#         }
#         return render(request, self.template_name, context)


# class Config(View):
#     template_name = 'account/config.html'
#
#     def get(self, request):
#         if is_employer(request.user):
#             profile = request.user.profile
#             context = {
#                 'form': ProfileEditForm(instance=profile)
#             }
#         else:
#             context = {}
#         return render(request, self.template_name, context)
#
#     def post(self, request):
#         profile = request.user.profile
#         form = ProfileEditForm(request.POST, request.FILES, instance=profile)
#
#         if form.is_valid():
#             form.save()
#             return redirect('account:config')
#
#         return render(request, self.template_name)


class EmailVerify(View):
    def get(self, request, uidb64, token):
        user = self.get_user(uidb64)

        if user is not None and default_token_generator.check_token(user, token):
            user.email_verify = True
            user.save()
            login(request, user)
            return redirect('service:feed')

        return redirect('account:invalid_verify')

    @staticmethod
    def get_user(uidb64):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError,
                User.DoesNotExist, ValidationError):
            user = None

        return user


class Register(FormView):
    template_name = 'registration/register.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('account:confirm_email')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            messages.error(self.request, 'Такой Email уже существует')
            return self.render_to_response(self.get_context_data(form=form))
        else:
            user = form.save(commit=False)
            user.username = email
            user.save()
            user_type = form.cleaned_data['user_type']
            if user_type == 'E':
                self.create_employer_profile(user)
            send_email_for_verify(self.request, user)
            return super().form_valid(form)

    @staticmethod
    def create_employer_profile(user):
        EmployerProfile.objects.create(user=user)


class Login(View):
    template_name = 'registration/login.html'
    form_class = UserLoginForm

    def get(self, request):
        context = {'form': self.form_class()}

        return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            return self.handle_authenticated_user(user)
        context = {'form': form}

        return render(request, self.template_name, context)

    def handle_authenticated_user(self, user):
        if not user:
            messages.error(self.request, 'Invalid email or password')
            return render(self.request, self.template_name, {'form': self.form_class()})

        if not user.is_active:
            messages.error(self.request, 'Account is disabled')
            return render(self.request, self.template_name, {'form': self.form_class()})

        if not user.email_verify:
            send_email_for_verify(self.request, user)
            return redirect('account:confirm_email')

        login(self.request, user)

        return redirect('service:feed')


class Config(View):
    template_name = 'account/config.html'

    def get(self, request):
        profile = request.user.profile
        context = {'form': ProfileEditForm(instance=profile)}

        return render(request, self.template_name, context)

    def post(self, request):
        profile = request.user.profile
        form = ProfileEditForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            form.save()
            return redirect('account:config')
        context = {'form': form}

        return render(request, self.template_name, context)


@login_required
def user_logout(request):
    logout(request)

    return redirect('service:feed')
