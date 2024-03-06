from app.internal.models.checking_account import CheckingAccount
from app.internal.models.card import Card
from asgiref.sync import sync_to_async


async def try_get_card_balance(card_number: int) -> str:
    try:
        card = await Card.objects.aget(card_number=card_number)
        return f"Баланс на карте: {card.balance}"
    except Card.DoesNotExist:
        return "Карта с указанным номером не найдена в базе данных"


@sync_to_async
def get_checking_account_cards_balance(account_number: int) -> str:
    checking_account = CheckingAccount.objects.filter(account_number=account_number).first()
    if checking_account is None:
        return "Рассчетный счет не существует"
    cards = Card.objects.filter(checking_account=checking_account)
    return f"Баланс на рассчетном счете: {sum([card.balance for card in cards])}"
