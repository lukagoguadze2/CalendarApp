from user.forms import UpdateProfileForm
from user.utils import get_country_code
from .auth import AuthView, AuthLogout, AuthRegisterView
from .auth import *

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, RedirectView, DetailView, UpdateView

from user.models import User
from user.hasher import decode_user_hash


def index(request):
    return render(request, 'calendar.html')


class DashboardView(TemplateView):
    template_name = 'dashboard.html'


class NewEventView(TemplateView):
    template_name = 'secondary_pages/page-new-event.html'


class AddEventView(TemplateView):
    template_name = 'secondary_pages/page-add-event.html'


@method_decorator(login_required(login_url='frontend:authentication:login'), name='dispatch')
class ProfileRedirectView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse(
            'frontend:profile:about',
            kwargs=self.request.user.get_profile_slug(dict_=True)  # custom method from User model
        )


class ProfileView(DetailView):
    model = User
    template_name = 'contact/contact-detail.html'
    context_object_name = 'profile'
    slug_field = 'hash'
    slug_url_kwarg = 'hash'

    def get_object(self, queryset=None):
        # User can see their own profile regardless of the is_private field
        if self.request.user.is_authenticated and self.kwargs['hash'] in self.request.user.get_profile_slug():
            return self.request.user

        return get_object_or_404(
            User,
            id=decode_user_hash(self.kwargs['hash']),
            is_private=False  # Only public profiles can be viewed
        )


class ProfileSettingsView(UpdateView):
    model = User
    template_name = 'profile_settings.html'
    form_class = UpdateProfileForm
    success_url = reverse_lazy('frontend:profile:settings')

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['phone_country_code'] = get_country_code(
            getattr(self.get_object(), 'phone_number', None)
        )
        return context


class ContactListView(TemplateView):
    template_name = 'contact/contact-list.html'
