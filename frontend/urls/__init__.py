from django.urls import path, include
from django.views.generic import TemplateView

from frontend.views import (
    index,
    ProfileRedirectView,
    ContactListView
)

app_name = 'frontend'

urlpatterns = [
    path('', index, name='index'),
    path('auth/', include('frontend.urls.authentication', namespace='authentication')),
    path('dashboard/', include('frontend.urls.dashboard')),
    path('contact-list/', ContactListView.as_view(), name='contact-list'),
    path('notifications/', TemplateView.as_view(template_name='notifications.html'), name='notifications'),
    path('me/', ProfileRedirectView.as_view(), name='profile-redirect'),
    path('profile/', include('frontend.urls.profile', namespace='profile')),
    path('service-unavailable/', TemplateView.as_view(template_name='pages/pages-maintenance.html'), name='maintenance'),
]
