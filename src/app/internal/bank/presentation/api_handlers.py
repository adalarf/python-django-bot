from django.http.response import JsonResponse
from app.internal.bank.domain.messages import BankMessage
from app.internal.bank.domain.service import BankService
from django.http import HttpRequest
from tests.utils import make_async_to_sync


class BankAPIHandlers:
    def __init__(self, bank_service: BankService):
        self._bank_service = bank_service

    def transfer_by_account(self, request: HttpRequest):
        user_account = request.POST.get("user_account")
        favorite_account = request.POST.get("favorite_account")
        money_amount = request.POST.get("money_amount")
        transfer = make_async_to_sync(self._bank_service.transfer_by_checking_account(
            user_account, favorite_account, money_amount))

        return JsonResponse({"data": transfer})

    def get_account_balance(self, request: HttpRequest, account_number: str):
        if len(account_number) != 20:
            return JsonResponse({"data": BankMessage.checking_account_incorrect_length_message()})
        else:
            checking_account = make_async_to_sync(self._bank_service.try_get_checking_account_balance(account_number))
            return JsonResponse({"data": checking_account})
