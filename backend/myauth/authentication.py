from typing import Optional

from django.http.request import HttpRequest
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import AuthUser, JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import Token


class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request: HttpRequest) -> Optional[tuple[AuthUser, Token]]:
        raw_token = request.COOKIES.get('access')
        if raw_token is None:
            return None

        try:
            validated_token = self.get_validated_token(raw_token)
            user = self.get_user(validated_token)
        except TokenError as exc:
            # TokenError — включает истечение срока, неверную подпись и т.д.
            raise AuthenticationFailed(detail=str(exc)) from exc
        except InvalidToken as exc:
            raise AuthenticationFailed(detail="Invalid token") from exc

        if user is None:
            raise AuthenticationFailed(detail="User not found")

        if not getattr(user, "is_active", True):
            raise AuthenticationFailed(detail="User is inactive")

        return user, validated_token
