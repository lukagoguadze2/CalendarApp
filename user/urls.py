from django.urls import path

from user.views import RemovePhoneNumber

app_name = 'user'

urlpatterns = [
    path('remove_phone_number/', RemovePhoneNumber.as_view(), name='remove_phone_number'),
]
