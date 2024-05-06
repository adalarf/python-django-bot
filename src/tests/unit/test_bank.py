import pytest
from app.internal.services.bank_service import try_get_card_balance, try_get_checking_account_balance,\
    get_user_checking_accounts
from app.internal.services.message_service import Message
from tests.utils import make_async_to_sync


@pytest.mark.unit
@pytest.mark.django_db
def test_get_checking_account_balance(create_first_account):
    account_number = create_first_account.account_number
    checking_account = make_async_to_sync(try_get_checking_account_balance(account_number))
    assert checking_account == Message.checking_account_balance_message(create_first_account)


@pytest.mark.unit
@pytest.mark.django_db
def test_get_does_not_exist_checking_account_balance():
    account_number = "00045678901234567890"
    checking_account = make_async_to_sync(try_get_checking_account_balance(account_number))
    assert checking_account == Message.checking_account_not_fount_message()


@pytest.mark.unit
@pytest.mark.django_db
def test_get_card_balance(create_first_card):
    card_number = create_first_card.card_number
    card = make_async_to_sync(try_get_card_balance(card_number))
    assert card == Message.card_balance_message(create_first_card)


@pytest.mark.unit
@pytest.mark.django_db
def test_get_does_not_exist_card_balance():
    card_number = "0004567812345678"
    card = make_async_to_sync(try_get_card_balance(card_number))
    assert card == Message.card_not_fount_message()


@pytest.mark.unit
@pytest.mark.django_db
def test_get_user_checking_accounts(create_first_account, create_first_user):
    favorite_accounts = get_user_checking_accounts(create_first_user.id)
    assert list(favorite_accounts)[0]["account_number"] == create_first_account.account_number
