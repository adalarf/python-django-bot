from app.internal.models.user import User
from asgiref.sync import sync_to_async
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


async def get_user_info(user_id: int) -> list|str:
    user = await get_user(user_id)
    if user.phone_number is None:
        return "Для просмотра информации о профиле введите номер телефона"
    return f"Ваш id - {user.id}\n" \
           f"Ваше имя - {user.name}\n" \
           f"Ваш номер телефона - {user.phone_number}"


def validate_phone(phone: str) -> bool:
    phone_number_pattern = r"^(\+.)?\d{10}$"
    return re.fullmatch(phone_number_pattern, phone) is not None