class AuthMessage:
    @staticmethod
    def password_or_name_not_provided_message():
        return "Имя или пароль не предоставлены"

    @staticmethod
    def wrong_password_message():
        return "Неверный пароль"

    @staticmethod
    def password_is_set_message():
        return "Пароль установлен"

    @staticmethod
    def token_not_found_message():
        return "Токен не найден"

    @staticmethod
    def revoke_all_tokens_message():
        return "Все токены удалены"

    @staticmethod
    def token_expired_message():
        return "Завершен срок действия токена"

    @staticmethod
    def password_not_provided_message():
        return "Пароль не предоставлен"
