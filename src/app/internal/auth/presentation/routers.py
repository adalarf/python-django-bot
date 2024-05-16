from ninja import Router
from app.internal.auth.presentation.api_handlers import AuthAPIHandlers


def get_auth_router(auth_handler: AuthAPIHandlers):
    router = Router(tags=["auth"])

    router.add_api_operation(
        "/login/",
        ["POST"],
        auth_handler.login,
        auth=None,
    )

    router.add_api_operation(
        "/refresh/",
        ["POST"],
        auth_handler.refresh,
        auth=None,
    )

    return router
