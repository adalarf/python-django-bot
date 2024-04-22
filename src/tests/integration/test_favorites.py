import pytest
from app.internal.services.user_service import add_user_to_favorite_list
from tests.utils import make_async_to_sync
from app.internal.transport.bot.handlers import add_favorite_user, get_favorite_users, delete_favorite_user
from app.internal.services.message_service import Message


@pytest.mark.integration
@pytest.mark.django_db
def test_add_user_to_favorite_mock(mock_update, mock_context, create_first_user, create_second_user):
    mock_context.args = [create_second_user.name]
    make_async_to_sync(add_favorite_user(mock_update, mock_context))
    mock_update.message.reply_text.assert_called_once_with(Message.added_favorite_user_message())


@pytest.mark.integration
@pytest.mark.django_db
def test_add_does_not_exist_user_to_favorite_mock(mock_update, mock_context, create_first_user):
    mock_context.args = ["test_user_name"]
    make_async_to_sync(add_favorite_user(mock_update, mock_context))
    mock_update.message.reply_text.assert_called_once_with(Message.user_not_found_message())


@pytest.mark.integration
@pytest.mark.django_db
def test_delete_user_from_favorite_mock(mock_update, mock_context, create_first_user, create_second_user):
    make_async_to_sync(add_user_to_favorite_list(create_first_user.id, create_second_user.name))
    mock_context.args = [create_second_user.name]
    make_async_to_sync(delete_favorite_user(mock_update, mock_context))
    mock_update.message.reply_text.assert_called_once_with(Message.deleted_favorite_user_message())


@pytest.mark.integration
@pytest.mark.django_db
def test_delete_does_not_exist_user_from_favorite_mock(mock_update, mock_context, create_first_user):
    mock_context.args = ["test_user_name"]
    make_async_to_sync(delete_favorite_user(mock_update, mock_context))
    mock_update.message.reply_text.assert_called_once_with(Message.user_not_found_message())


@pytest.mark.integration
@pytest.mark.django_db
def test_get_favorite_users_without_favorites_mock(mock_update, mock_context, create_first_user):
    make_async_to_sync(get_favorite_users(mock_update, mock_context))
    mock_update.message.reply_text.assert_called_once_with(Message.none_favorites_message())


@pytest.mark.integration
@pytest.mark.django_db
def test_get_favorite_users_with_favorites_mock(mock_update, mock_context,
                                                create_first_user, create_second_user):
    make_async_to_sync(add_user_to_favorite_list(create_first_user.id, create_second_user.name))
    make_async_to_sync(get_favorite_users(mock_update, mock_context))
    mock_update.message.reply_text.assert_called_once_with(create_second_user.name)
