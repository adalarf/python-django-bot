from telegram import Update
from telegram.ext import CallbackContext
from app.internal.services.user_service import update_or_create_user, get_user, set_phone_from_user, validate_phone, get_user_info


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

