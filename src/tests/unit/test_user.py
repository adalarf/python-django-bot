import pytest
from app.internal.users.domain.service import UsersService, get_users_service
from app.internal.users.domain.messages import UsersMessage
from tests.utils import make_async_to_sync


@pytest.mark.unit
@pytest.mark.django_db
def test_get_does_not_exist_user():
    is_exist = make_async_to_sync(get_users_service().is_user_exists(9999))
    assert is_exist is False


@pytest.mark.unit
@pytest.mark.django_db
def test_get_user_info(create_first_user):
    user_info = make_async_to_sync(UsersService.get_user_info(get_users_service(), create_first_user.id))
    assert user_info == UsersMessage.user_info_message(create_first_user)


@pytest.mark.unit
@pytest.mark.django_db
def test_get_user_info_without_phone(create_user_without_phone):
    user_info = make_async_to_sync(UsersService.get_user_info(get_users_service(), create_user_without_phone.id))
    assert user_info == UsersMessage.phone_required_message()
