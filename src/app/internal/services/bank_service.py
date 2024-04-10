import decimal

from django.db import transaction

from app.internal.models.checking_account import CheckingAccount
from app.internal.models.card import Card
from app.internal.models.user import User
from asgiref.sync import sync_to_async
from .message_service import Message
from .user_service import is_favorite, get_user


@sync_to_async
def try_get_card_balance(card_number: int) -> str:
    try:
        card = Card.objects.get(card_number=card_number)
        return Message.card_balance_message(card)
    except Card.DoesNotExist:
        return Message.card_not_fount_message()


async def try_get_checking_account_balance(account_number: str) -> str:
    try:
        checking_account = await CheckingAccount.objects.aget(account_number=account_number)
        return Message.checking_account_balance_message(checking_account)
    except:
        return Message.checking_account_not_fount_message()


def get_user_checking_accounts(favorite: User) -> list:
    favorite_accounts = CheckingAccount.objects.filter(owner=favorite)
    favorite_accounts = [i.account_number for i in favorite_accounts]
    return favorite_accounts


@sync_to_async
def transfer_by_name(favorite_name: str) -> str:
    favorite = User.objects.filter(name=favorite_name).first()
    if not favorite:
        return Message.user_not_found_message()
    favorite_accounts = get_user_checking_accounts(favorite)
    return Message.favorite_accounts_message(favorite_accounts)


@sync_to_async
def transfer_by_checking_account(user_account: str, favorite_account: str, money_amount: decimal.Decimal) -> str:
    favorite_account = CheckingAccount.objects.filter(account_number=favorite_account).first()
    user_account = CheckingAccount.objects.filter(account_number=user_account).first()
    if not favorite_account or not user_account:
        return Message.checking_account_not_fount_message()
    if not is_favorite(user_account.owner, favorite_account.owner):
        return Message.user_is_not_favorite_message()
    else:
        make_transfer(user_account, favorite_account, money_amount)
        return Message.transfer_successful_message()


@transaction.atomic
def make_transfer(user_account: CheckingAccount, favorite_account: CheckingAccount, money_amount: decimal.Decimal) -> None:
    user_account.balance -= decimal.Decimal(money_amount)
    favorite_account.balance += decimal.Decimal(money_amount)
    user_account.save()
    favorite_account.save()
