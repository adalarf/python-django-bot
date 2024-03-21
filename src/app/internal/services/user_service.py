from app.internal.models.user import User
from asgiref.sync import sync_to_async
from .message_service import Message
import re


async def update_or_create_user(user_id: int, user_name: str) -> (User, bool):
    return await User.objects.aupdate_or_create(id=user_id, defaults={"id": user_id, "name": user_name})


async def get_user(user_id: int) -> User:
    return await User.objects.aget(id=user_id)


@sync_to_async
def is_user_exists(user_id: int) -> bool:
    return User.objects.filter(id=user_id).exists()


async def set_phone_from_user(user: User, user_phone_number: int) -> None:
    user.phone_number = user_phone_number
    await user.asave()


async def get_user_info(user_id: int) -> list | str:
    user = await get_user(user_id)
    if user.phone_number is None:
        return Message.phone_required_message()
    return Message.user_info_message(user)


def validate_phone(phone: str) -> bool:
    phone_number_pattern = r"^(\+.)?\d{10}$"
    return re.fullmatch(phone_number_pattern, phone) is not None


async def get_favorite_user(favorite_name: str) -> str | User:
    favorite_user = await User.objects.filter(name=favorite_name).afirst()
    if not favorite_user:
        return Message.user_not_found_message()
    return favorite_user


async def add_user_to_favorite_list(user_id: int, favorite_name: str):
    favorite_user = await get_favorite_user(favorite_name)
    user = await get_user(user_id)
    await user.favorite_users.aadd(favorite_user)
    await user.asave()


async def delete_user_from_favorite_list(user_id: int, favorite_name: str) -> str:
    favorite_user = await get_favorite_user(favorite_name)
    user = await get_user(user_id)
    await user.favorite_users.aremove(favorite_user)
    await user.asave()
    return Message.deleted_favorite_user_message()


async def is_favorite(user: User, favorite_user: User) -> bool:
    favorite_user = user.favorite_users.filter(user__id=favorite_user.id).afirst()
    return favorite_user


async def get_favorite_users_list(user_id: int):
    user = await get_user(user_id)
    favorite_users = user.favorite_users.all()
    is_empty = await favorite_users.aexists()
    if not is_empty:
        return Message.none_favorites_message()
    return favorite_users
