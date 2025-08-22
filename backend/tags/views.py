from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Tag
from .serializers import TagSerializer


class TagView(APIView):
    def get(self, request: Request, *args, **kwargs) -> Response:
        queryset = Tag.objects.all()

        serializer = TagSerializer(queryset, many=True)
        return Response({'tags': serializer.data}, status=status.HTTP_200_OK)
