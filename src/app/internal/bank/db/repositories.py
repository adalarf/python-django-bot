from app.internal.bank.db.models import CheckingAccount, Card, Transaction
from app.internal.users.db.models import User
from django.core.files.base import ContentFile
from decimal import Decimal
from datetime import datetime
from django.db import transaction
from django.db.models import F
import abc


class IBankRepository(abc.ABC):
    @abc.abstractmethod
    def get_card(self, card_number: int):
        pass

    @abc.abstractmethod
    async def get_checking_account(self, account_number: str):
        pass

    @abc.abstractmethod
    def get_user_checking_accounts(self, favorite: User):
        pass

    @abc.abstractmethod
    def get_favorite_account(self, favorite_account: str):
        pass

    @abc.abstractmethod
    def get_user_account(self, user_account: str):
        pass

    @abc.abstractmethod
    def make_transfer(self, user_account: CheckingAccount,
                      favorite_account: CheckingAccount, money_amount: Decimal, postcard: bytes, path: str):
        pass

    @abc.abstractmethod
    def make_transactions_viewed(self, transactions: list) -> None:
        pass

    @abc.abstractmethod
    async def get_new_transactions(self, account_number: str) -> list:
        pass

    @abc.abstractmethod
    def get_checking_account_statement(self, account_number: str, date_start: datetime, date_end: datetime):
        pass

    @abc.abstractmethod
    def get_interacted_users(self, account_number: list) -> list:
        pass


class BankRepository(IBankRepository):
    def get_card(self, card_number: int) -> Card:
        return Card.objects.get(card_number=card_number)

    async def get_checking_account(self, account_number: str) -> CheckingAccount:
        return await CheckingAccount.objects.aget(account_number=account_number)

    def get_user_checking_accounts(self, favorite: User) -> list:
        favorite_accounts = CheckingAccount.objects.filter(owner__id=favorite).values("account_number")
        return favorite_accounts

    def get_favorite_account(self, favorite_account: str) -> list:
        return CheckingAccount.objects.filter(account_number=favorite_account).first()

    def get_user_account(self, user_account: str) -> list:
        return CheckingAccount.objects.filter(account_number=user_account).first()

    @transaction.atomic
    def make_transfer(self, user_account: CheckingAccount,
                      favorite_account: CheckingAccount, money_amount: Decimal,
                      postcard: bytes, postcard_type: str) -> None:
        user_account.balance = F("balance") - Decimal(money_amount)
        favorite_account.balance = F("balance") + Decimal(money_amount)
        user_account.save(update_fields=("balance",))
        favorite_account.save(update_fields=("balance",))
        transaction = Transaction.objects.create(sender_account=user_account, receiver_account=favorite_account,
                                                 money_amount=money_amount, datetime=datetime.now())
        if postcard:
            transaction.postcard.save(f"{transaction.id}.{postcard_type}", ContentFile(postcard))

    def make_transactions_viewed(self, transactions: list) -> None:
        for transaction_item in transactions:
            transaction_item.is_viewed = True
            transaction_item.save()

    def get_new_transactions(self, account_number: str) -> list:
        checking_account = CheckingAccount.objects.get(account_number=account_number)
        transactions = Transaction.objects.filter(sender_account=checking_account,
                                                  is_viewed=False)
        return list(transactions)

    def get_checking_account_statement(self, account_number: str, date_start: datetime, date_end: datetime) -> list:
        checking_account = CheckingAccount.objects.get(account_number=account_number)
        transactions = Transaction.objects.filter(sender_account=checking_account,
                                                  datetime__gte=date_start,
                                                  datetime__lte=date_end
                                                  ).values("receiver_account__account_number",
                                                           "money_amount", "datetime")
        return list(transactions)

    def get_interacted_users(self, account_number: list) -> list:
        checking_account = CheckingAccount.objects.get(account_number=account_number)
        receiver_transactions = Transaction.objects.filter(sender_account=checking_account)\
            .values("sender_account__account_number", "receiver_account__account_number", "money_amount", "datetime")
        sender_transactions = Transaction.objects.filter(receiver_account=checking_account)\
            .values("sender_account__account_number", "receiver_account__account_number", "money_amount", "datetime")
        transactions = receiver_transactions.union(sender_transactions).order_by("datetime")

        return list(transactions)
