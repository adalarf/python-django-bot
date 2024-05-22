from app.internal.bank.db.models import CheckingAccount, Card
from app.internal.users.db.models import User
from asgiref.sync import sync_to_async
from app.internal.bank.domain.messages import BankMessage
from app.internal.users.domain.service import UsersService, get_users_service
from app.internal.users.domain.messages import UsersMessage
from app.internal.bank.db.repositories import BankRepository, IBankRepository
from datetime import datetime
from decimal import Decimal


class BankService:
    def __init__(self, bank_repository: IBankRepository, users_service: UsersService):
        self._bank_repository = bank_repository
        self._users_service = users_service

    @sync_to_async
    def try_get_card_balance(self, card_number: int) -> str:
        try:
            card = self._bank_repository.get_card(card_number)
            return BankMessage.card_balance_message(card)
        except Card.DoesNotExist:
            return BankMessage.card_not_fount_message()

    async def try_get_checking_account_balance(self, account_number: str) -> str:
        try:
            checking_account = await self._bank_repository.get_checking_account(account_number)
            return BankMessage.checking_account_balance_message(checking_account)
        except:
            return BankMessage.checking_account_not_fount_message()

    def get_user_checking_accounts(self, favorite: User) -> list:
        return self._bank_repository.get_user_checking_accounts(favorite)

    @sync_to_async
    def transfer_by_name(self, favorite_name: str) -> str:
        favorite = self._users_service.get_favorite_user_id(favorite_name)
        if not favorite:
            return UsersMessage.user_not_found_message()
        favorite_accounts = self.get_user_checking_accounts(favorite["id"])
        return BankMessage.favorite_accounts_message(favorite_accounts)

    @sync_to_async
    def transfer_by_checking_account(self, user_account: str, favorite_account: str, money_amount: Decimal, postcard: bytes = None, postcard_type: str = None) -> str:
        favorite_account = self._bank_repository.get_favorite_account(favorite_account)
        user_account = self._bank_repository.get_user_account(user_account)
        if not favorite_account or not user_account:
            return BankMessage.checking_account_not_fount_message()
        if not self._users_service.is_favorite(user_account.owner, favorite_account.owner):
            return UsersMessage.user_is_not_favorite_message()
        else:
            self.make_transfer(user_account, favorite_account, money_amount, postcard, postcard_type)
            return BankMessage.transfer_successful_message()

    def make_transfer(self, user_account: CheckingAccount,
                      favorite_account: CheckingAccount, money_amount: Decimal, postcard: bytes, postcard_type: str) -> None:
        self._bank_repository.make_transfer(user_account, favorite_account, money_amount, postcard, postcard_type)

    def make_transactions_viewed(self, transactions: list) -> None:
        self._bank_repository.make_transactions_viewed(transactions)

    @sync_to_async
    def get_new_transactions(self, account_number: str):
        transactions = self._bank_repository.get_new_transactions(account_number)
        self.make_transactions_viewed(transactions)
        return transactions

    @sync_to_async
    def get_checking_account_statement(self, account_number: str, date_start: datetime, date_end: datetime) -> list:
        return self._bank_repository.get_checking_account_statement(account_number, date_start, date_end)

    @sync_to_async
    def get_interacted_users(self, account_number: list) -> list:
        return self._bank_repository.get_interacted_users(account_number)


def get_bank_service() -> BankService:
    return BankService(BankRepository(), get_users_service())
