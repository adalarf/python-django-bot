from telegram import Update
from telegram.ext import CallbackContext
from app.internal.services.user_service import update_or_create_user, get_user, set_phone_from_user, validate_phone,\
    get_user_info, add_user_to_favorite_list, delete_user_from_favorite_list, get_favorite_users_list
from app.internal.services.bank_service import try_get_card_balance, try_get_checking_account_balance,\
    transfer_by_checking_account, transfer_by_name, get_checking_account_statement, get_interacted_users
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


async def transfer_money_by_name(update: Update, context: CallbackContext) -> None:
    favorite_name = context.args[0]
    favorite_accounts = await transfer_by_name(favorite_name)
    await update.message.reply_text(favorite_accounts)


async def transfer_money_by_checking_account(update: Update, context: CallbackContext) -> None:
    user_account = context.args[0]
    favorite_account = context.args[1]
    money_amount = context.args[2]
    transfer = await transfer_by_checking_account(user_account, favorite_account, money_amount)
    await update.message.reply_text(transfer)


async def add_favorite_user(update: Update, context: CallbackContext):
    user = update.effective_user
    favorite_name = context.args[0]
    if await add_user_to_favorite_list(user.id, favorite_name) != Message.user_not_found_message():
        await update.message.reply_text(Message.added_favorite_user_message())
    else:
        await update.message.reply_text(Message.user_not_found_message())


async def delete_favorite_user(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    favorite_name = context.args[0]
    if await delete_user_from_favorite_list(user.id, favorite_name) != Message.user_not_found_message():
        await update.message.reply_text(Message.deleted_favorite_user_message())
    else:
        await update.message.reply_text(Message.user_not_found_message())


async def get_favorite_users(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    favorites = await get_favorite_users_list(user.id)
    if favorites == Message.none_favorites_message():
        await update.message.reply_text(favorites)
    else:
        message = ""
        async for favorite in favorites:
            message += f"{favorite.name}"
        await update.message.reply_text(message)


async def get_account_statement(update: Update, context: CallbackContext) -> None:
    checking_account = context.args[0]
    date_start = context.args[1]
    date_end = context.args[2]
    statement = await get_checking_account_statement(checking_account, date_start, date_end)
    statement = list(statement)
    await update.message.reply_text(Message.statement_message(statement))


async def get_users_interacted_with(update: Update, context: CallbackContext) -> None:
    checking_account = context.args[0]
    interacted_users = await get_interacted_users(checking_account)
    interacted_users_list = list(interacted_users)
    await update.message.reply_text(Message.interacted_users_message(interacted_users_list))
