from app.internal.users.db.models import User


class UsersMessage:
    @staticmethod
    def user_not_found_message():
        return "Пользователь не найден"

    @staticmethod
    def phone_required_message():
        return "Для просмотра информации о профиле введите номер телефона"

    @staticmethod
    def user_info_message(user: User):
        return f"Ваш id - {user.id}\n" \
               f"Ваше имя - {user.name}\n" \
               f"Ваш номер телефона - {user.phone_number}"

    @staticmethod
    def added_favorite_user_message():
        return "Пользователь добавлен в избранное"

    @staticmethod
    def deleted_favorite_user_message():
        return "Пользователь удален из избранного"

    @staticmethod
    def user_is_not_favorite_message():
        return "Пользователя нет в избранном"

    @staticmethod
    def none_favorites_message():
        return "Пользователей в избранном нет"

    @staticmethod
    def name_added_to_db_message(user: User):
        return f"Ваше имя {user.first_name} добавлено в базу данных"

    @staticmethod
    def incorrect_phone_format_message():
        return "Некорректный формат номера. Введите номер в формате: '+XXXXXXXXXXX'"

    @staticmethod
    def phone_added_to_db_message(user: User):
        return f"Ваш телефон {user.phone_number} добавлен в базу данных"

    @staticmethod
    def phone_already_added_to_db_message():
        return "Ваш телефон уже был добавлен в базу данных"
