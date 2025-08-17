from django.contrib.auth import authenticate, get_user_model
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView

from config import settings
from myauth.serializers import LoginSerializer, RegisterSerializer, UserSerializer


COOKIE_OPTIONS = {
    'httponly': True,
    'secure': getattr(settings, 'COOKIE_SECURE', False),
    'samesite': getattr(settings, 'COOKIE_SAMESITE', 'Lax'),
}


class LoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request: Request):
        User = get_user_model()
        data = request.data.get('user', {})
        serializer = LoginSerializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as ex:
            return Response({'errors': ex.detail}, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        try:
            user = User.objects.get(email=email)
            username = user.get_username()
        except User.DoesNotExist:
            return Response({'errors': {'message': 'User not found'}}, status=status.HTTP_404_NOT_FOUND)

        user = authenticate(request=request, username=username, password=password)
        if user is None:
            return Response({'errors': {'message': 'Invalid credentials'}}, status=status.HTTP_400_BAD_REQUEST)

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        user_data = UserSerializer(user).data
        response = Response({'user': user_data}, status=status.HTTP_200_OK)
        response.set_cookie('refresh', refresh_token, **COOKIE_OPTIONS)
        response.set_cookie('access', access_token, **COOKIE_OPTIONS)
        return response


class CookieTokenRefreshView(TokenRefreshView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request: Request, *args, **kwargs) -> Response:
        refresh_token = request.COOKIES.get('refresh')
        if not refresh_token:
            return Response({'errors': {'token': 'Refresh token not provided'}},
                            status=status.HTTP_401_UNAUTHORIZED)

        serializer = self.get_serializer(data={'refresh': refresh_token})
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response({'errors': {'token': 'Invalid refresh token'}}, status=status.HTTP_401_UNAUTHORIZED)

        response = Response(status=status.HTTP_200_OK)

        access = serializer.validated_data.get('access')
        response.set_cookie('access', access, **COOKIE_OPTIONS)

        return response


class RegistrationView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request: Request, *args, **kwargs) -> Response:
        data = request.data.get('user', {})
        serializer = RegisterSerializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
        except ValidationError as ex:
            return Response({'errors': ex.detail}, status=status.HTTP_400_BAD_REQUEST)

        user_data = UserSerializer(user).data
        response = Response({'user': user_data}, status=status.HTTP_201_CREATED)
        return response


class LogoutView(APIView):
    def post(self, request: Request):
        response = Response(status=status.HTTP_200_OK)
        response.delete_cookie('access')
        response.delete_cookie('refresh')
        return response
