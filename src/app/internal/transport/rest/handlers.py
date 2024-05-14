from django.http.response import JsonResponse
from app.internal.services.message_service import Message
from app.internal.services.user_service import make_password_hashed
from app.internal.services.auth_service import generate_access_token, generate_refresh_token, get_issued_token, \
    get_user_id_by_token, create_issued_token, is_token_expired, revoke_all_tokens_by_user_id, revoke_token
from app.internal.models.user import User
from .middleware import HTTPJWTAuth
from ninja import NinjaAPI


api = NinjaAPI()


@api.get("me/", auth=HTTPJWTAuth())
def me(request):
    user = request.user
    if user is None:
        return JsonResponse({"error": Message.user_not_found_message()}, status=404)
    return JsonResponse({"data": Message.user_info_message(user)}, status=200)


@api.post("login/", auth=None)
def login(request):
    name = request.POST.get("name")
    password = request.POST.get("password")
    if name is None or password is None:
        return JsonResponse({"error": Message.password_or_name_not_provided_message()}, status=400)

    user = User.objects.filter(name=name).first()
    if user is None:
        return JsonResponse({"error": Message.user_not_found_message()}, status=404)
    if not user.password == make_password_hashed(password):
        return JsonResponse({"error": Message.wrong_password_message()}, status=401)

    access_token = generate_access_token(user.id)
    refresh_token = generate_refresh_token(user.id)
    create_issued_token(user, refresh_token)

    data = {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user_name": name
    }

    return JsonResponse(data, status=200)


@api.post("refresh/", auth=None)
def refresh(request):
    refresh_token = request.POST.get("token")
    issued_token = get_issued_token(refresh_token)
    if not issued_token:
        return JsonResponse({"error": Message.token_not_found_message()}, status=404)

    user_id = get_user_id_by_token(issued_token)

    if issued_token.revoked:
        revoke_all_tokens_by_user_id(user_id)
        return JsonResponse({"data": Message.revoke_all_tokens_message()}, status=200)

    revoke_token(issued_token)

    if is_token_expired(issued_token):
        return JsonResponse({"error": Message.token_expired_message()}, status=400)

    access_token = generate_access_token(user_id)
    refresh_token = generate_refresh_token(user_id)
    data = {
        "access_token": access_token,
        "refresh_token": refresh_token
    }

    return JsonResponse(data, status=200)
