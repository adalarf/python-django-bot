from telegram.ext import CommandHandler, ApplicationBuilder

from app.internal.transport.bot.handlers import start, set_phone, get_info, get_card_balance,\
    get_checking_account_balance, transfer_money_by_checking_account, add_favorite_user, delete_favorite_user,\
    get_favorite_users
from config.settings import TELEGRAM_TOKEN


def start_bot():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("set_phone", set_phone))
    app.add_handler(CommandHandler("me", get_info))
    app.add_handler(CommandHandler("card_balance", get_card_balance))
    app.add_handler(CommandHandler("checking_account_balance", get_checking_account_balance))
    app.add_handler(CommandHandler("transfer", transfer_money_by_checking_account))
    app.add_handler(CommandHandler("add_favorite", add_favorite_user))
    app.add_handler(CommandHandler("delete_favorite", delete_favorite_user))
    app.add_handler(CommandHandler("favorites", get_favorite_users))

    app.run_polling()
