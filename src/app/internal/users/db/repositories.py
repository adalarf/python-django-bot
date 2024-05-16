from app.internal.users.db.models import User
import abc


class IUsersRepository(abc.ABC):
    @abc.abstractmethod
    async def update_or_create_user(self, user_id: int, user_name: str) -> (User, bool):
        pass

    @abc.abstractmethod
    async def get_user(self, user_id: int) -> User:
        pass

    @abc.abstractmethod
    def is_user_exists(self, user_id: int) -> bool:
        pass

    @abc.abstractmethod
    async def get_favorite_user(self, favorite_name: str) -> User:
        pass

    @abc.abstractmethod
    def is_favorite(self, user: User, favorite_user: User) -> bool:
        pass

    @abc.abstractmethod
    def get_favorite_user_id(self, favorite_name) -> User:
        pass


class UsersRepository(IUsersRepository):
    async def update_or_create_user(self, user_id: int, user_name: str) -> (User, bool):
        return await User.objects.aupdate_or_create(id=user_id, defaults={"id": user_id, "name": user_name})

    async def get_user(self, user_id: int) -> User:
        return await User.objects.aget(id=user_id)

    def is_user_exists(self, user_id: int) -> bool:
        return User.objects.filter(id=user_id).exists()

    async def get_favorite_user(self, favorite_name: str) -> User:
        return await User.objects.filter(name=favorite_name).afirst()

    def is_favorite(self, user: User, favorite_user: User) -> bool:
        return user.favorite_users.filter(id=favorite_user.id).exists()

    def get_favorite_user_id(self, favorite_name) -> User:
        return User.objects.filter(name=favorite_name).values("id").first()
