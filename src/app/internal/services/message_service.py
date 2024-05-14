from app.internal.models.user import User
from app.internal.models.checking_account import CheckingAccount
from app.internal.models.card import Card
from app.internal.models.transaction import Transaction


class Message:
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

    @staticmethod
    def checking_account_incorrect_format_message():
        return "Некорректный ввод - введите счет как последовательность из 20 цифр"

    @staticmethod
    def checking_account_incorrect_length_message():
        return "Некорректный ввод - в рассчетном счете 20 цифр"

    @staticmethod
    def card_incorrect_format_message():
        return "Некорректный ввод - введите номер карты как последовательность из 16 цифр"

    @staticmethod
    def card_incorrect_length_message():
        return "Некорректный ввод - в номере карты 16 цифр"

    @staticmethod
    def phone_required_message():
        return "Для просмотра информации о профиле введите номер телефона"

    @staticmethod
    def user_info_message(user: User):
        return f"Ваш id - {user.id}\n" \
               f"Ваше имя - {user.name}\n" \
               f"Ваш номер телефона - {user.phone_number}"

    @staticmethod
    def checking_account_balance_message(checking_account: CheckingAccount):
        return f"Баланс на рассчетном счете: {checking_account.balance}"

    @staticmethod
    def checking_account_not_fount_message():
        return "Рассчетный счет с указанным номером не найден в базе данных"

    @staticmethod
    def card_balance_message(card: Card):
        return f"Баланс на карте: {card.checking_account.balance}"

    @staticmethod
    def card_not_fount_message():
        return "Карта с указанным номером не найдена в базе данных"

    @staticmethod
    def user_not_found_message():
        return "Пользователь не найден"

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
    def transfer_successful_message():
        return "Деньги переведены"

    @staticmethod
    def transaction_successful_message():
        return "Транзакция выполнена"

    @staticmethod
    def none_favorites_message():
        return "Пользователей в избранном нет"

    @staticmethod
    def favorite_accounts_message(favorite_accounts: list):
        return f"Рассчетные счета пользователя: {[i['account_number'] for i in favorite_accounts]}"

    @staticmethod
    def interacted_users_message(transactions: list):
        message = ""
        for i in transactions:
            message += f"От {i['sender_account__account_number']} К {i['receiver_account__account_number']}\n" \
                       f"Сумма: {i['money_amount']} Дата: {i['datetime'].strftime('%d-%m-%Y')}\n" \
                       f"--------------------------\n"
        return message

    @staticmethod
    def statement_message(statement: list):
        message = ""
        for i in statement:
            message += f"Дата: {i['datetime'].strftime('%d-%m-%Y')} " \
                       f"Получатель: {i['receiver_account__account_number']}\n" \
                       f"Сумма: {i['money_amount']}\n" \
                       f"--------------------------\n"
        return message

    @staticmethod
    def password_not_provided_message():
        return "Пароль не предоставлен"

    @staticmethod
    def password_is_set_message():
        return "Пароль установлен"

    @staticmethod
    def password_or_name_not_provided_message():
        return "Имя или пароль не предоставлены"

    @staticmethod
    def wrong_password_message():
        return "Неверный пароль"

    @staticmethod
    def token_not_found_message():
        return "Токен не найден"

    @staticmethod
    def revoke_all_tokens_message():
        return "Все токены удалены"

    @staticmethod
    def token_expired_message():
        return "Завершен срок действия токена"
