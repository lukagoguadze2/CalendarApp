from django.http import Http404
from django.conf import settings
from django.urls import reverse_lazy
from django.shortcuts import redirect

from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.views import LoginView, LogoutView

from django.utils import timezone
from django.utils.decorators import method_decorator

from django.views.generic.edit import FormView
from django.views.generic import CreateView, UpdateView

from user.models import PasswordResetSession
from user.tasks import expire_password_reset_session, send_password_reset_email_task
from user.forms import (
    PasswordResetForm,
    UpdatePasswordForm,
    RegistrationForm,
    SecondStageRegistrationForm
)

from user.models import User


class AuthView(LoginView):
    template_name = 'authentication/login.html'
    form_class = AuthenticationForm
    next_page = 'frontend:index'
    redirect_authenticated_user = True

    def form_valid(self, form):
        x = super().form_valid(form)  # ჯერ შევიყვანოთ იუზერი ექაუნთში
        self.request.user.last_activity = timezone.now()  # შემდეგ შევუცვალოთ ბოლო აქტივობა
        self.request.user.save()  # ამით middleware არ დაალოგაუთებს პირველივე რექუესტზე
        return x


class AuthLogout(LogoutView):
    template_name = 'authentication/logout.html'
    next_page = 'frontend:authentication:login'
    http_method_names = LogoutView.http_method_names + ['get']

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('frontend:authentication:login')


# თუ მომხმარებელი ხელით გადავა რეგისტრაციზე როდესაც ექაუნთშია შესული მაშინ დეკორატორი გადაამისამართეს LOGOUT-ის გვერდზე
@method_decorator(
    user_passes_test(lambda u: u.is_anonymous, login_url='frontend:authentication:logout'),
    name='dispatch'
)
class AuthRegisterView(CreateView):
    model = User
    form_class = RegistrationForm
    template_name = 'authentication/sign-up.html'
    success_url = reverse_lazy('frontend:index')

    def form_valid(self, form):
        x = super().form_valid(form)
        self.object.is_staff = True
        self.object.save()
        login(self.request, self.object)  # შევიყვანოთ მომხმარებელი ექაუნთში რეგისტრაციის შემდეგ
        return x


class SecondStageRegisterView(UpdateView):
    model = User
    form_class = SecondStageRegistrationForm
    template_name = 'authentication/register_fully.html'
    success_url = reverse_lazy('frontend:index')

    def dispatch(self, request, *args, **kwargs):
        if getattr(request.user, 'is_fully_registered', True):
            raise Http404('You are already fully registered or not logged in.')

        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        x = super().form_valid(form)
        self.object.is_fully_registered = True
        self.object.save()
        return x


class PasswordResetRequestView(FormView):
    template_name = 'authentication/password-reset.html'
    form_class = PasswordResetForm
    success_url = reverse_lazy('frontend:authentication:password-reset-confirm')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        user = User.objects.get(email=email)

        # წავშალოთ წინა სესიები
        PasswordResetSession.objects.filter(
            user=user,
            is_expired=False
        ).delete()

        # შევქმნათ ახალი სესია და გავაგზავნოთ ელ. წერილი პაროლის განახლების ლინკით
        new_session = PasswordResetSession.generate_token(user)

        # დავაგენერიროთ ლინკი
        reset_url = self.request.build_absolute_uri(
            reverse_lazy('frontend:authentication:password-reset-session', kwargs={'token': new_session.token})
        )

        # გავუშვათ სელერის ტასკი, რათა დახუროს სესია {PASSWORD_RESET_SESSION_TIMEOUT} წამში
        task = expire_password_reset_session.apply_async(
            (new_session.token,),
            countdown=settings.PASSWORD_RESET_SESSION_TIMEOUT
        )

        # დავაყენოთ სელერის ტასკის ID სესიაში
        new_session.celery_task_id = task.id
        new_session.save()

        # გავაგზავნოთ ელ. წერილი სელერით
        send_password_reset_email_task.apply_async(
            (
                email,
                reset_url,
                user.first_name,
                self.request.build_absolute_uri('/'),
                self.request.META.get('HTTP_USER_AGENT')
            )
        )

        return super().form_valid(form)


class ResetPasswordView(UpdateView):
    model = User
    form_class = UpdatePasswordForm
    template_name = 'authentication/update-password-page.html'
    success_url = reverse_lazy('frontend:authentication:login')

    def get_object(self, queryset=None):
        try:
            return PasswordResetSession.objects.get(token=self.kwargs['token']).user
        except PasswordResetSession.DoesNotExist:
            raise Http404('Link is invalid or expired.')

    def form_valid(self, form):
        x = super().form_valid(form)
        user = self.get_object()
        user.set_password(form.cleaned_data['password1']), user.save()
        PasswordResetSession.objects.get(token=self.kwargs['token']).delete()
        return x
