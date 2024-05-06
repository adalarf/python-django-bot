from django.http import HttpRequest
from ninja.security import HttpBearer
from app.internal.models.user import User
from app.internal.services.auth_service import get_payload


class HTTPJWTAuth(HttpBearer):
    def authenticate(self, request: HttpRequest, token):
        try:
            payload = get_payload(token)
            user_id = payload["sub"]
            user = User.objects.get(id=user_id)
            request.user = user
        except:
            return None

        return token
