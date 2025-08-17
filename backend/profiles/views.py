from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request: Request):
    user = getattr(request, 'user', None)
    return Response({
        'user': {
            'email': user.email,
            'username': user.get_username(),
            'bio': getattr(user, 'bio', ''),
            'image': getattr(user, 'image', None),
        }
    })
