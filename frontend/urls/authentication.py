from django.urls import path
from django.views.generic import TemplateView
from frontend.views import AuthView, AuthLogout, AuthRegisterView
from frontend.views.auth import SecondStageRegisterView, PasswordResetRequestView, ResetPasswordView
from frontend.views import auth as auth_views
app_name = 'authentication'

urlpatterns = [
    path('login/', AuthView.as_view(), name='login'),
    path('logout/', AuthLogout.as_view(), name='logout'),
    path('register/', AuthRegisterView.as_view(), name='register'),
    path('register/stage-2/', SecondStageRegisterView.as_view(), name='register_fully'),
    path('reset-password/', PasswordResetRequestView.as_view(), name='password-reset'),
    path('reset-password/<str:token>/', ResetPasswordView.as_view(), name='password-reset-session'),
    path('password-reset-confirm/', TemplateView.as_view(template_name='authentication/auth-confirm-mail.html'), name='password-reset-confirm'),
    path('lock-screen/', TemplateView.as_view(template_name='authentication/lock-screen.html'), name='lock-screen'),
]
