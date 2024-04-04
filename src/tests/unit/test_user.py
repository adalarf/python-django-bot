import pytest
from app.internal.services.user_service import is_user_exists, get_user_info
from app.internal.services.message_service import Message
from tests.utils import make_async_to_sync


@pytest.mark.django_db
def test_get_does_not_exist_user():
    is_exist = make_async_to_sync(is_user_exists(9999))
    assert is_exist is False


@pytest.mark.django_db
def test_get_user_info(create_first_user):
    user_info = make_async_to_sync(get_user_info(create_first_user.id))
    assert user_info == Message.user_info_message(create_first_user)


@pytest.mark.django_db
def test_get_user_info_without_phone(create_user_without_phone):
    user_info = make_async_to_sync(get_user_info(create_user_without_phone.id))
    assert user_info == Message.phone_required_message()
