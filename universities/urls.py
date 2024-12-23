from django.urls import path
from universities.views import LoadFaculties

app_name = 'universities'

urlpatterns = [
    path('load-faculties/', LoadFaculties.as_view(), name='load-faculties'),
]
