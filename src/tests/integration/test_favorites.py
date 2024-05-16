import pytest
from app.internal.users.domain.service import UsersService, get_users_service
from tests.utils import make_async_to_sync
from app.internal.users.presentation.bot_handlers import UsersBotHandlers
from app.internal.users.domain.messages import UsersMessage


@pytest.mark.integration
@pytest.mark.django_db
def test_add_user_to_favorite_mock(mock_update, mock_context, create_first_user, create_second_user):
    mock_context.args = [create_second_user.name]
    make_async_to_sync(UsersBotHandlers.add_favorite_user(UsersBotHandlers(get_users_service()),
                                                          mock_update, mock_context))
    mock_update.message.reply_text.assert_called_once_with(UsersMessage.added_favorite_user_message())


@pytest.mark.integration
@pytest.mark.django_db
def test_add_does_not_exist_user_to_favorite_mock(mock_update, mock_context, create_first_user):
    mock_context.args = ["test_user_name"]
    make_async_to_sync(UsersBotHandlers.add_favorite_user(UsersBotHandlers(get_users_service()),
                                                          mock_update, mock_context))
    mock_update.message.reply_text.assert_called_once_with(UsersMessage.user_not_found_message())


@pytest.mark.integration
@pytest.mark.django_db
def test_delete_user_from_favorite_mock(mock_update, mock_context, create_first_user, create_second_user):
    make_async_to_sync(UsersService.add_user_to_favorite_list(get_users_service(), create_first_user.id,
                                                              create_second_user.name))
    mock_context.args = [create_second_user.name]
    make_async_to_sync(UsersBotHandlers.delete_favorite_user(UsersBotHandlers(get_users_service()),
                                                             mock_update, mock_context))
    mock_update.message.reply_text.assert_called_once_with(UsersMessage.deleted_favorite_user_message())


@pytest.mark.integration
@pytest.mark.django_db
def test_delete_does_not_exist_user_from_favorite_mock(mock_update, mock_context, create_first_user):
    mock_context.args = ["test_user_name"]
    make_async_to_sync(UsersBotHandlers.delete_favorite_user(UsersBotHandlers(get_users_service()),
                                                             mock_update, mock_context))
    mock_update.message.reply_text.assert_called_once_with(UsersMessage.user_not_found_message())


@pytest.mark.integration
@pytest.mark.django_db
def test_get_favorite_users_without_favorites_mock(mock_update, mock_context, create_first_user):
    make_async_to_sync(UsersBotHandlers.get_favorite_users(UsersBotHandlers(get_users_service()),
                                                           mock_update, mock_context))
    mock_update.message.reply_text.assert_called_once_with(UsersMessage.none_favorites_message())


@pytest.mark.integration
@pytest.mark.django_db
def test_get_favorite_users_with_favorites_mock(mock_update, mock_context,
                                                create_first_user, create_second_user):
    make_async_to_sync(UsersService.add_user_to_favorite_list(get_users_service(), create_first_user.id,
                                                              create_second_user.name))
    make_async_to_sync(UsersBotHandlers.get_favorite_users(UsersBotHandlers(get_users_service()),
                                                           mock_update, mock_context))
    mock_update.message.reply_text.assert_called_once_with(create_second_user.name)
