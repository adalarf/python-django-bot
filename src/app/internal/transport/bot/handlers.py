from telegram import Update
from telegram.ext import CallbackContext
from app.internal.services.user_service import update_or_create_user, get_user, set_phone_from_user, validate_phone, get_user_info
from app.internal.services.bank_service import try_get_card_balance, try_get_checking_account_balance
from app.internal.services.message_service import Message


async def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    await update_or_create_user(user.id, user.first_name)
    await update.message.reply_text(Message.name_added_to_db_message(user))


async def set_phone(update: Update, context: CallbackContext) -> None:
    user = await get_user(update.effective_user.id)
    if len(context.args) == 0:
        await update.message.reply_text(Message.incorrect_phone_format_message())
        return
    phone_number = context.args[0]
    if not validate_phone(phone_number):
        await update.message.reply_text(Message.incorrect_phone_format_message())
    elif user.phone_number != phone_number:
        await set_phone_from_user(user, phone_number)
        await update.message.reply_text(Message.phone_added_to_db_message(user))
    else:
        await update.message.reply_text(Message.phone_already_added_to_db_message())


async def get_info(update: Update, context: CallbackContext) -> None:
    user_info = await get_user_info(update.effective_user.id)
    await update.message.reply_text(user_info)


async def get_card_balance(update: Update, context: CallbackContext) -> None:
    if len(context.args) == 0:
        await update.message.reply_text(Message.card_incorrect_format_message())
        return
    card_number = context.args[0]
    if len(card_number) != 16:
        await update.message.reply_text(Message.card_incorrect_length_message())
    else:
        card_balance = await try_get_card_balance(card_number)
        await update.message.reply_text(card_balance)


async def get_checking_account_balance(update: Update, context: CallbackContext) -> None:
    if len(context.args) == 0:
        await update.message.reply_text(Message.checking_account_incorrect_format_message())
        return
    account_number = context.args[0]
    if len(account_number) != 20:
        await update.message.reply_text(Message.checking_account_incorrect_length_message())
    else:
        checking_account = await try_get_checking_account_balance(account_number)
        await update.message.reply_text(checking_account)
