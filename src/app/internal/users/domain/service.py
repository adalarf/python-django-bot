from app.internal.users.db.models import User
from app.internal.users.domain.messages import UsersMessage
from app.internal.users.db.repositories import UsersRepository, IUsersRepository
from asgiref.sync import sync_to_async
from config import settings
import hashlib
import re


class UsersService:
    def __init__(self, users_repository: IUsersRepository):
        self._users_repository = users_repository

    async def update_or_create_user(self, user_id: int, user_name: str) -> (User, bool):
        return await self._users_repository.update_or_create_user(user_id, user_name)

    async def get_user(self, user_id: int) -> User:
        return await self._users_repository.get_user(user_id)

    @sync_to_async
    def is_user_exists(self, user_id: int) -> bool:
        return self._users_repository.is_user_exists(user_id)

    async def set_phone_from_user(self, user: User, user_phone_number: int) -> None:
        user.phone_number = user_phone_number
        await user.asave()

    def make_password_hashed(self, password: str) -> str:
        return hashlib.sha256(password.encode() + settings.SALT.encode()).hexdigest()

    async def set_user_password(self, user_id: int, password: str) -> None:
        try:
            user = await self.get_user(user_id)
            user.password = self.make_password_hashed(password)
            await user.asave()
        except User.DoesNotExist:
            raise UsersMessage.user_not_found_message()

    async def get_user_info(self, user_id: int) -> list | str:
        user = await self.get_user(user_id)
        if user.phone_number is None:
            return UsersMessage.phone_required_message()
        return UsersMessage.user_info_message(user)

    def validate_phone(self, phone: str) -> bool:
        phone_number_pattern = r"^(\+.)?\d{10}$"
        return re.fullmatch(phone_number_pattern, phone) is not None

    async def get_favorite_user(self, favorite_name: str) -> str | User:
        favorite_user = await self._users_repository.get_favorite_user(favorite_name)
        if not favorite_user:
            return UsersMessage.user_not_found_message()
        return favorite_user

    async def add_user_to_favorite_list(self, user_id: int, favorite_name: str) -> None:
        favorite_user = await self.get_favorite_user(favorite_name)
        if favorite_user == UsersMessage.user_not_found_message():
            return UsersMessage.user_not_found_message()
        user = await self.get_user(user_id)
        await user.favorite_users.aadd(favorite_user)
        await user.asave()

    async def delete_user_from_favorite_list(self, user_id: int, favorite_name: str) -> str:
        favorite_user = await self.get_favorite_user(favorite_name)
        if favorite_user == UsersMessage.user_not_found_message():
            return UsersMessage.user_not_found_message()
        user = await self.get_user(user_id)
        await user.favorite_users.aremove(favorite_user)
        await user.asave()
        return UsersMessage.deleted_favorite_user_message()

    def is_favorite(self, user: User, favorite_user: User) -> bool:
        return self._users_repository.is_favorite(user, favorite_user)

    def get_favorite_user_id(self, favorite_name) -> User:
        return self._users_repository.get_favorite_user_id(favorite_name)

    async def get_favorite_users_list(self, user_id: int) -> str | User:
        user = await self.get_user(user_id)
        favorite_users = user.favorite_users.all()
        is_empty = await favorite_users.aexists()
        if not is_empty:
            return UsersMessage.none_favorites_message()
        return favorite_users


def get_users_service() -> UsersService:
    return UsersService(UsersRepository())
