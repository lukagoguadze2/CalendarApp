from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from user.permissions import IsOwner


class RemovePhoneNumber(APIView):
    http_method_names = ['patch']
    permission_classes = [IsAuthenticated, IsOwner]

    def get_object(self):
        return self.request.user

    def patch(self, request, *args, **kwargs):
        user = self.get_object()
        user.phone_number = None
        user.save()
        return Response({'success': True})
