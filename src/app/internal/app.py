from ninja import NinjaAPI
from .auth.domain.middleware import HTTPJWTAuth
from .auth.presentation.routers import get_auth_router
from .users.presentation.routers import get_user_router
from .bank.presentation.routers import get_bank_router
from .auth.presentation.api_handlers import AuthAPIHandlers
from .users.presentation.api_handlers import UsersAPIHandlers
from .bank.presentation.api_handlers import BankAPIHandlers
from .auth.domain.service import get_auth_service
from .users.domain.service import get_users_service
from .bank.domain.service import get_bank_service


def get_api():
    api = NinjaAPI()
    auth = HTTPJWTAuth(get_auth_service())
    users_router = get_user_router(UsersAPIHandlers(get_users_service()), auth)
    auth_router = get_auth_router(AuthAPIHandlers(get_auth_service(), get_users_service()))
    bank_router = get_bank_router(BankAPIHandlers(get_bank_service()), auth)
    api.add_router("/users/", users_router)
    api.add_router("/auth/", auth_router)
    api.add_router("/bank/", bank_router)
    return api


api = get_api()
