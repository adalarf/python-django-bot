from asgiref.sync import sync_to_async
from app.internal.bank.db.models import CheckingAccount, Card


class BankMessage:
    @staticmethod
    def card_balance_message(card: Card):
        return f"Баланс на карте: {card.checking_account.balance}"

    @staticmethod
    def card_not_fount_message():
        return "Карта с указанным номером не найдена в базе данных"

    @staticmethod
    def checking_account_balance_message(checking_account: CheckingAccount):
        return f"Баланс на рассчетном счете: {checking_account.balance}"

    @staticmethod
    def checking_account_not_fount_message():
        return "Рассчетный счет с указанным номером не найден в базе данных"

    @staticmethod
    def favorite_accounts_message(favorite_accounts: list):
        return f"Рассчетные счета пользователя: {[i['account_number'] for i in favorite_accounts]}"

    @staticmethod
    def transfer_successful_message():
        return "Деньги переведены"

    @staticmethod
    def transaction_successful_message():
        return "Транзакция выполнена"

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
    @sync_to_async
    def get_new_transactions_message(transactions: list):
        message = ""
        if not transactions:
            return "Новых транзакций нет"
        for i in transactions:
            message += f"Дата: {i.datetime.strftime('%d-%m-%Y')} " \
                       f"Получатель: {i.receiver_account.account_number}\n" \
                       f"Сумма: {i.money_amount}\n"
            if i.postcard:
                message += f"Ссылка: {i.postcard.url}\n"
            message += "--------------------------\n"
        return message
