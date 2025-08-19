from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Tag


class TagView(APIView):
    def get(self, request: Request, *args, **kwargs) -> Response:
        tags = Tag.objects.values_list('tag', flat=True)
        return Response({'tags': tags}, status=status.HTTP_200_OK)
