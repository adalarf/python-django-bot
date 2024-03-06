from telegram import Update
from telegram.ext import CallbackContext
from app.internal.services.user_service import update_or_create_user, get_user, set_phone_from_user, validate_phone, get_user_info
from app.internal.services.bank_service import try_get_card_balance, get_checking_account_cards_balance


async def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    await update_or_create_user(user.id, user.first_name)
    await update.message.reply_text(f"Ваше имя {user.first_name} добавлено в базу данных")


async def set_phone(update: Update, context: CallbackContext) -> None:
    user = await get_user(update.effective_user.id)
    if len(context.args) == 0:
        await update.message.reply_text("Некорректный формат номера. Введите номер в формате: '+XXXXXXXXXXX'")
        return
    phone_number = context.args[0]
    if not validate_phone(phone_number):
        await update.message.reply_text("Некорректный формат номера. Введите номер в формате: '+XXXXXXXXXXX'")
    elif user.phone_number != phone_number:
        await set_phone_from_user(user, phone_number)
        await update.message.reply_text(f"Ваш телефон {user.phone_number} добавлен в базу данных")
    else:
        await update.message.reply_text("Ваш телефон уже был добавлен в базу данных")


async def get_info(update: Update, context: CallbackContext) -> None:
    user_info = await get_user_info(update.effective_user.id)
    await update.message.reply_text(user_info)


async def get_card_balance(update: Update, context: CallbackContext) -> None:
    if len(context.args) == 0:
        await update.message.reply_text("Некорректный ввод - введите номер карты как последовательность из 16 цифр")
        return
    card_number = context.args[0]
    if len(card_number) != 16:
        await update.message.reply_text("Некорректный ввод - в номере карты 16 цифр")
    else:
        card_balance = await try_get_card_balance(card_number)
        await update.message.reply_text(card_balance)


async def get_checking_account_balance(update: Update, context: CallbackContext) -> None:
    if len(context.args) == 0:
        await update.message.reply_text("Некорректный ввод - введите счет как последовательность из 20 цифр")
        return
    account_number = context.args[0]
    if len(account_number) != 20:
        await update.message.reply_text("Некорректный ввод - в рассчетном счете 20 цифр")
    else:
        checking_account = await get_checking_account_cards_balance(account_number)
        await update.message.reply_text(checking_account)