import pytest
from app.internal.services.user_service import add_user_to_favorite_list
from app.internal.services.bank_service import transfer_by_checking_account, transfer_by_name,\
    get_user_checking_accounts
from app.internal.services.message_service import Message
from tests.utils import make_async_to_sync
from decimal import Decimal


@pytest.mark.integration
@pytest.mark.django_db
def test_transfer_by_checking_account(create_first_user, create_second_user,
                                      create_first_account, create_second_account):
    make_async_to_sync(add_user_to_favorite_list(create_first_user.id, create_second_user.name))
    transfer = make_async_to_sync(transfer_by_checking_account(
        create_first_account.account_number, create_second_account.account_number,
        money_amount=Decimal("100.00").quantize(Decimal("0.01"))))
    assert transfer == Message.transfer_successful_message()


@pytest.mark.integration
@pytest.mark.django_db
def test_transfer_not_favorite_by_checking_account(create_first_user, create_second_user,
                                                   create_first_account, create_second_account):
    transfer = make_async_to_sync(transfer_by_checking_account(
        create_first_account.account_number, create_second_account.account_number,
        money_amount=Decimal("100.00").quantize(Decimal("0.01"))))
    assert transfer == Message.user_is_not_favorite_message()


@pytest.mark.integration
@pytest.mark.django_db
def test_transfer_by_name(create_second_user):
    transfer = make_async_to_sync(transfer_by_name(create_second_user.name))
    favorite_accounts = get_user_checking_accounts(create_second_user)
    assert transfer == Message.favorite_accounts_message(favorite_accounts)
