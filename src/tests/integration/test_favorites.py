import pytest
from telegram import Update
from app.internal.services.user_service import add_user_to_favorite_list, is_favorite, delete_user_from_favorite_list
from tests.utils import make_async_to_sync
from app.internal.transport.bot.handlers import add_favorite_user
from app.internal.services.message_service import Message


@pytest.mark.integration
@pytest.mark.django_db
def test_add_user_to_favorite_mock(mock_update: Update, mock_context, create_first_user, create_second_user):
    mock_context.args = [create_second_user.name]
    make_async_to_sync(add_favorite_user(mock_update, mock_context))
    mock_update.message.reply_text.assert_called_once_with(Message.added_favorite_user_message())


@pytest.mark.integration
@pytest.mark.django_db
def test_delete_user_from_favorite(create_first_user, create_second_user):
    make_async_to_sync(add_user_to_favorite_list(create_first_user.id, create_second_user.name))
    make_async_to_sync(delete_user_from_favorite_list(create_first_user.id, create_second_user.name))
    is_favorite_user = is_favorite(create_first_user, create_second_user)
    assert is_favorite_user is False
