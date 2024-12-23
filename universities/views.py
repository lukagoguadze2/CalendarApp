from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from universities.models import Faculty, Course
from universities.serializers import FacultySerializer, GetFacultiesSerializer


class LoadFaculties(ListAPIView):
    serializer_class = FacultySerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        filter_data = GetFacultiesSerializer(data=self.request.GET)
        if (
                not filter_data.is_valid(raise_exception=True) or
                not Course.objects.filter(
                    degree_level=filter_data.validated_data['level_of_study'],
                    faculty__university_id=filter_data.validated_data['university_id']
                ).exists()
        ):
            return Faculty.objects.none()

        return Faculty.objects.filter(
            university_id=filter_data.validated_data['university_id'],
            course__degree_level=filter_data.validated_data['level_of_study']
        ).distinct()
