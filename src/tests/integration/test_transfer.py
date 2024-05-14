import pytest
from app.internal.users.domain.service import UsersService, get_users_service
from app.internal.bank.domain.messages import BankMessage
from app.internal.users.domain.messages import UsersMessage
from tests.utils import make_async_to_sync
from decimal import Decimal
from app.internal.bank.domain.service import get_bank_service
from app.internal.bank.presentation.bot_handlers import BankBotHandlers


@pytest.mark.integration
@pytest.mark.django_db
def test_transfer_by_checking_account_mock(mock_update, mock_context, create_first_user, create_second_user,
                                           create_first_account, create_second_account):
    make_async_to_sync(UsersService.add_user_to_favorite_list(get_users_service(), create_first_user.id,
                                                              create_second_user.name))
    mock_context.args = [create_first_account.account_number, create_second_account.account_number,
                         Decimal("100.00").quantize(Decimal("0.01"))]
    make_async_to_sync(BankBotHandlers.transfer_money_by_checking_account(BankBotHandlers(get_bank_service()),
                                                                          mock_update, mock_context))
    mock_update.message.reply_text.assert_called_once_with(BankMessage.transfer_successful_message())


@pytest.mark.integration
@pytest.mark.django_db
def test_transfer_not_favorite_by_checking_account_mock(mock_update, mock_context,
                                                        create_first_user, create_second_user,
                                                        create_first_account, create_second_account):
    mock_context.args = [create_first_account.account_number, create_second_account.account_number,
                         Decimal("100.00").quantize(Decimal("0.01"))]
    make_async_to_sync(BankBotHandlers.transfer_money_by_checking_account(BankBotHandlers(get_bank_service()),
                                                                          mock_update, mock_context))
    mock_update.message.reply_text.assert_called_once_with(UsersMessage.user_is_not_favorite_message())


@pytest.mark.integration
@pytest.mark.django_db
def test_transfer_by_does_not_exist_checking_account_mock(mock_update, mock_context, create_first_user,
                                                          create_second_user, create_first_account):
    mock_context.args = [create_first_account.account_number, "00045678901234567890",
                         Decimal("100.00").quantize(Decimal("0.01"))]
    make_async_to_sync(BankBotHandlers.transfer_money_by_checking_account(BankBotHandlers(get_bank_service()),
                                                                          mock_update, mock_context))
    mock_update.message.reply_text.assert_called_once_with(BankMessage.checking_account_not_fount_message())


@pytest.mark.integration
@pytest.mark.django_db
def test_transfer_by_name_mock(mock_update, mock_context, create_first_user, create_first_account):
    mock_context.args = [create_first_user.name]
    make_async_to_sync(BankBotHandlers.transfer_money_by_name(BankBotHandlers(get_bank_service()),
                                                              mock_update, mock_context))
    mock_update.message.reply_text.assert_called_once_with(BankMessage.favorite_accounts_message(
        [{"account_number": create_first_account.account_number}]))


@pytest.mark.integration
@pytest.mark.django_db
def test_transfer_does_not_exist_user_by_name_mock(mock_update, mock_context):
    mock_context.args = ["test_user_name"]
    make_async_to_sync(BankBotHandlers.transfer_money_by_name(BankBotHandlers(get_bank_service()),
                                                              mock_update, mock_context))
    mock_update.message.reply_text.assert_called_once_with(UsersMessage.user_not_found_message())
