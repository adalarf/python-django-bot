from app.internal.models.checking_account import CheckingAccount
from app.internal.models.card import Card
from asgiref.sync import sync_to_async
from .message_service import Message

@sync_to_async
def try_get_card_balance(card_number: int) -> str:
    try:
        card = Card.objects.get(card_number=card_number)
        return Message.card_balance_message(card)
    except Card.DoesNotExist:
        return Message.card_not_fount_message()


# @sync_to_async
# def get_checking_account_cards_balance(account_number: int) -> str:
#     checking_account = CheckingAccount.objects.filter(account_number=account_number).first()
#     if checking_account is None:
#         return "Рассчетный счет не существует"
#     cards = Card.objects.filter(checking_account=checking_account)
#     return f"Баланс на рассчетном счете: {sum([card.balance for card in cards])}"

async def try_get_checking_account_balance(account_number: str) -> str:
    try:
        checking_account = await CheckingAccount.objects.aget(account_number=account_number)
        return Message.checking_account_balance_message(checking_account)
    except:
        return Message.checking_account_not_fount_message()