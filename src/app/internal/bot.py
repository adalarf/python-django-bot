from telegram.ext import CommandHandler, ApplicationBuilder

from app.internal.transport.bot.handlers import start, set_phone, get_info, get_card_balance,\
    get_checking_account_balance
from config.settings import TELEGRAM_TOKEN


def start_bot():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("set_phone", set_phone))
    app.add_handler(CommandHandler("me", get_info))
    app.add_handler(CommandHandler("card_balance", get_card_balance))
    app.add_handler(CommandHandler("checking_account_balance", get_checking_account_balance))

    app.run_polling()
