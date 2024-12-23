from rest_framework import serializers
from universities.models import Faculty, Course, University


class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = ('id', 'name')


class GetFacultiesSerializer(serializers.Serializer):
    university_id = serializers.IntegerField()
    level_of_study = serializers.CharField()

    @staticmethod
    def validate_university_id(value):
        if not University.objects.filter(pk=value).exists():
            raise serializers.ValidationError('Invalid university id.')

        return value

    @staticmethod
    def validate_level_of_study(value):
        if value.upper() not in map(lambda _: _[0], Course.degree_level_choice):
            raise serializers.ValidationError('Invalid level of study.')

        return value.upper()
