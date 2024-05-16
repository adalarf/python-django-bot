from ninja import Router
from app.internal.bank.presentation.api_handlers import BankAPIHandlers
from app.internal.auth.domain.middleware import HTTPJWTAuth


def get_bank_router(bank_handler: BankAPIHandlers, auth: HTTPJWTAuth):
    router = Router(tags=["bank"])

    router.add_api_operation(
        "/transfer/",
        ["POST"],
        bank_handler.transfer_by_account,
        auth=auth,
    )

    router.add_api_operation(
        "/account_balance/{account_number}/",
        ["GET"],
        bank_handler.get_account_balance,
        auth=auth,
    )

    return router
