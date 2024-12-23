from rest_framework import serializers

from user.models import Group


class GroupSerializer(serializers.ModelSerializer):
    group_type_display = serializers.CharField(source='get_group_type_display')

    class Meta:
        model = Group
        fields = ('id', 'name', 'group_type', 'group_type_display')
