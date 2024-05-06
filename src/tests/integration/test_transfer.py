import pytest
from app.internal.services.user_service import add_user_to_favorite_list
from app.internal.services.message_service import Message
from tests.utils import make_async_to_sync
from decimal import Decimal
from app.internal.transport.bot.handlers import transfer_money_by_checking_account, transfer_money_by_name


@pytest.mark.integration
@pytest.mark.django_db
def test_transfer_by_checking_account_mock(mock_update, mock_context, create_first_user, create_second_user,
                                           create_first_account, create_second_account):
    make_async_to_sync(add_user_to_favorite_list(create_first_user.id, create_second_user.name))
    mock_context.args = [create_first_account.account_number, create_second_account.account_number,
                         Decimal("100.00").quantize(Decimal("0.01"))]
    make_async_to_sync(transfer_money_by_checking_account(mock_update, mock_context))
    mock_update.message.reply_text.assert_called_once_with(Message.transfer_successful_message())


@pytest.mark.integration
@pytest.mark.django_db
def test_transfer_not_favorite_by_checking_account_mock(mock_update, mock_context,
                                                        create_first_user, create_second_user,
                                                        create_first_account, create_second_account):
    mock_context.args = [create_first_account.account_number, create_second_account.account_number,
                         Decimal("100.00").quantize(Decimal("0.01"))]
    make_async_to_sync(transfer_money_by_checking_account(mock_update, mock_context))
    mock_update.message.reply_text.assert_called_once_with(Message.user_is_not_favorite_message())


@pytest.mark.integration
@pytest.mark.django_db
def test_transfer_by_does_not_exist_checking_account_mock(mock_update, mock_context, create_first_user,
                                                          create_second_user, create_first_account):
    mock_context.args = [create_first_account.account_number, "00045678901234567890",
                         Decimal("100.00").quantize(Decimal("0.01"))]
    make_async_to_sync(transfer_money_by_checking_account(mock_update, mock_context))
    mock_update.message.reply_text.assert_called_once_with(Message.checking_account_not_fount_message())


# @pytest.mark.integration
# @pytest.mark.django_db
# def test_transfer_by_name_mock(mock_update, mock_context, create_first_user, create_first_account):
#     mock_context.args = [create_first_user.name]
#     make_async_to_sync(transfer_money_by_name(mock_update, mock_context))
#     mock_update.message.reply_text.assert_called_once_with(Message.favorite_accounts_message(
#         [create_first_account.account_number]))


@pytest.mark.integration
@pytest.mark.django_db
def test_transfer_does_not_exist_user_by_name_mock(mock_update, mock_context):
    mock_context.args = ["test_user_name"]
    make_async_to_sync(transfer_money_by_name(mock_update, mock_context))
    mock_update.message.reply_text.assert_called_once_with(Message.user_not_found_message())
