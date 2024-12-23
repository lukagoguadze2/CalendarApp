from django.urls import path

from frontend.views import ProfileView, ProfileSettingsView

app_name = 'profile'

urlpatterns = [
    path('settings/', ProfileSettingsView.as_view(), name='settings'),
    path('<str:username>-<str:hash>/', ProfileView.as_view(), name='about'),
]
