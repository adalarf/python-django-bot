from django.http.response import JsonResponse
from app.internal.users.domain.messages import UsersMessage
from app.internal.auth.domain.messages import AuthMessage
from app.internal.users.domain.service import UsersService
from django.http import HttpRequest
from tests.utils import make_async_to_sync


class UsersAPIHandlers:
    def __init__(self, users_service: UsersService):
        self._users_service = users_service

    def me(self, request: HttpRequest):
        user = request.user
        if user is None:
            return JsonResponse({"error": UsersMessage.user_not_found_message()}, status=404)
        return JsonResponse({"data": UsersMessage.user_info_message(user)}, status=200)

    def add_user_to_favorites(self, request: HttpRequest, favorite_name: str):
        user_id = request.user.id
        if make_async_to_sync(self._users_service.add_user_to_favorite_list(user_id, favorite_name))\
                != UsersMessage.user_not_found_message():
            return JsonResponse({"data": UsersMessage.added_favorite_user_message()})
        else:
            return JsonResponse({"data": UsersMessage.user_not_found_message()})

    def delete_user_from_favorites(self, request: HttpRequest, favorite_name: str):
        user_id = request.user.id
        if make_async_to_sync(self._users_service.delete_user_from_favorite_list(user_id, favorite_name))\
                != UsersMessage.user_not_found_message():
            return JsonResponse({"data": UsersMessage.deleted_favorite_user_message()})
        else:
            return JsonResponse({"data": UsersMessage.user_not_found_message()})

    def get_favorite_users(self, request: HttpRequest):
        user_id = request.user.id
        favorites = make_async_to_sync(self._users_service.get_favorite_users_list(user_id))
        if favorites == UsersMessage.none_favorites_message():
            return JsonResponse({"data": favorites})
        else:
            message = {}
            message["favorites"] = []
            for favorite in favorites:
                message["favorites"].append(favorite.name)
            return JsonResponse(message)

    def set_password(self, request: HttpRequest, password: str):
        user_id = request.user.id
        make_async_to_sync(self._users_service.set_user_password(user_id, password))
        return JsonResponse({"data": AuthMessage.password_is_set_message()})
