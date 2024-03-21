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


async def transfer_by_checking_account(user_account: str, favorite_account: str, money_amount: float):
    favorite_account = await CheckingAccount.objects.filter(account_number=favorite_account).afirst()
    user_account = await CheckingAccount.objects.filter(account_number=user_account).afirst()
    if not favorite_account or not user_account:
        return Message.checking_account_not_fount_message()
    if not is_favorite(user_account.owner, favorite_account.owner):
        return Message.user_is_not_favorite_message()
    else:
        user_account.balance -= money_amount
        favorite_account.balance += money_amount
        await user_account.asave()
        await favorite_account.asave()
        return Message.transfer_message()