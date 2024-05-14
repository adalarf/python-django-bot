from django.http.response import JsonResponse
from app.internal.auth.domain.messages import AuthMessage
from app.internal.auth.domain.service import AuthService
from app.internal.users.domain.service import UsersService
from app.internal.users.domain.messages import UsersMessage
from app.internal.users.db.models import User
from app.internal.auth.domain.entities import Tokens, TokensWithUser
from django.http import HttpRequest


class AuthAPIHandlers:
    def __init__(self, auth_service: AuthService, users_service: UsersService):
        self._auth_service = auth_service
        self._users_service = users_service

    def login(self, request: HttpRequest):
        name = request.POST.get("name")
        password = request.POST.get("password")
        if name is None or password is None:
            return JsonResponse({"error": AuthMessage.password_or_name_not_provided_message()}, status=400)

        user = User.objects.filter(name=name).first()
        if user is None:
            return JsonResponse({"error": UsersMessage.user_not_found_message()}, status=404)
        if not user.password == self._users_service.make_password_hashed(password):
            return JsonResponse({"error": AuthMessage.wrong_password_message()}, status=401)

        access_token = self._auth_service.generate_access_token(user.id)
        refresh_token = self._auth_service.generate_refresh_token(user.id)
        self._auth_service.create_issued_token(user, refresh_token)

        return TokensWithUser(access_token=access_token, refresh_token=refresh_token, user_name=name)

    def refresh(self, request: HttpRequest):
        refresh_token = request.POST.get("token")
        issued_token = self._auth_service.get_issued_token(refresh_token)
        if not issued_token:
            return JsonResponse({"error": AuthMessage.token_not_found_message()}, status=404)

        user_id = self._auth_service.get_user_id_by_token(issued_token)

        if issued_token.revoked:
            self._auth_service.revoke_all_tokens_by_user_id(user_id)
            return JsonResponse({"data": AuthMessage.revoke_all_tokens_message()}, status=200)

        self._auth_service.revoke_token(issued_token)

        if self._auth_service.is_token_expired(issued_token):
            return JsonResponse({"error": AuthMessage.token_expired_message()}, status=400)

        access_token = self._auth_service.generate_access_token(user_id)
        refresh_token = self._auth_service.generate_refresh_token(user_id)

        return Tokens(access_token=access_token, refresh_token=refresh_token)
