from django.urls import path
from frontend.views import DashboardView, NewEventView, AddEventView

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('add-new-event/', NewEventView.as_view(), name='add-new-event'),
    path('add-event/', AddEventView.as_view(), name='add-event'),
]
