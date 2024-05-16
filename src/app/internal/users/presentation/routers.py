from ninja import NinjaAPI, Router
from app.internal.users.presentation.api_handlers import UsersAPIHandlers
from app.internal.auth.domain.middleware import HTTPJWTAuth


def get_user_router(user_handler: UsersAPIHandlers, auth: HTTPJWTAuth):
    router = Router(tags=["auth"])

    router.add_api_operation(
        "/me/",
        ["GET"],
        user_handler.me,
        auth=auth,
    )

    router.add_api_operation(
        "/add-favorite/{favorite_name}/",
        ["POST"],
        user_handler.add_user_to_favorites,
        auth=auth,
    )

    router.add_api_operation(
        "/delete-favorite/{favorite_name}/",
        ["DELETE"],
        user_handler.delete_user_from_favorites,
        auth=auth,
    )

    router.add_api_operation(
        "/get-favorites/",
        ["GET"],
        user_handler.get_favorite_users,
        auth=auth,
    )

    router.add_api_operation(
        "/set-password/{password}/",
        ["PUT"],
        user_handler.set_password,
        auth=auth,
    )

    return router
