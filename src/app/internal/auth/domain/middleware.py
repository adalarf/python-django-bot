from app.internal.auth.domain.service import AuthService
from app.internal.users.db.models import User
from django.http import HttpRequest
from ninja.security import HttpBearer


class HTTPJWTAuth(HttpBearer):
    def __init__(self, auth_service: AuthService):
        self._auth_service = auth_service

    def authenticate(self, request: HttpRequest, token):
        try:
            payload = self._auth_service.get_payload(token)
            user_id = payload["sub"]
            user = User.objects.get(id=user_id)
            request.user = user
        except:
            return None

        return token
