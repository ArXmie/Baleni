from django.contrib.auth import get_user_model
from django.core import signing
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework.exceptions import AuthenticationFailed

TOKEN_MAX_AGE = 60 * 60 * 24 * 30


class TokenAuthentication(BaseAuthentication):
    keyword = b'bearer'

    def authenticate(self, request):
        parts = get_authorization_header(request).split()
        if not parts or parts[0].lower() != self.keyword:
            return None
        if len(parts) != 2:
            raise AuthenticationFailed('Неверный токен')
        try:
            data = signing.loads(parts[1].decode(), max_age=TOKEN_MAX_AGE)
        except (signing.BadSignature, UnicodeError):
            raise AuthenticationFailed('Неверный токен')
        user = get_user_model().objects.filter(pk=data.get('user_id'), is_active=True).first()
        if user is None:
            raise AuthenticationFailed('Пользователь не найден')
        return (user, None)

    def authenticate_header(self, request):
        return 'Bearer'
