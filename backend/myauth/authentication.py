from typing import Optional

from django.http.request import HttpRequest
from rest_framework_simplejwt.authentication import AuthUser, JWTAuthentication
from rest_framework import exceptions
from rest_framework_simplejwt.tokens import Token


class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request: HttpRequest) -> Optional[tuple[AuthUser, Token]]:
        raw_token = request.COOKIES.get('access')
        if raw_token is None:
            return None

        try:
            validated_token = self.get_validated_token(raw_token)
            user = self.get_user(validated_token)
            return user, validated_token
        except Exception as ex:
            raise exceptions.AuthenticationFailed('Invalid token from cookies') from ex
