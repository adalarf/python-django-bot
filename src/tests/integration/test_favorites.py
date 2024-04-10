import pytest
from app.internal.services.user_service import add_user_to_favorite_list, is_favorite, delete_user_from_favorite_list
from tests.utils import make_async_to_sync


@pytest.mark.integration
@pytest.mark.django_db
def test_add_user_to_favorite(create_first_user, create_second_user):
    make_async_to_sync(add_user_to_favorite_list(create_first_user.id, create_second_user.name))
    is_favorite_user = is_favorite(create_first_user, create_second_user)
    assert is_favorite_user is True


@pytest.mark.integration
@pytest.mark.django_db
def test_delete_user_from_favorite(create_first_user, create_second_user):
    make_async_to_sync(add_user_to_favorite_list(create_first_user.id, create_second_user.name))
    make_async_to_sync(delete_user_from_favorite_list(create_first_user.id, create_second_user.name))
    is_favorite_user = is_favorite(create_first_user, create_second_user)
    assert is_favorite_user is False
