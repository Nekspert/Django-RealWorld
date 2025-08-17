from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.request import Request


@api_view(['GET'])
@permission_classes([AllowAny])
def articles_list(request: Request):
    return Response({
        'articles': [],
        'articlesCount': 0
    })
