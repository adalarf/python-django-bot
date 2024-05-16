from telegram.ext import CommandHandler, ApplicationBuilder, MessageHandler, filters
from app.internal.users.presentation.bot_handlers import UsersBotHandlers
from app.internal.bank.presentation.bot_handlers import BankBotHandlers
from app.internal.users.domain.service import UsersService, get_users_service
from app.internal.bank.domain.service import BankService, get_bank_service
from config.settings import TELEGRAM_TOKEN


def start_bot():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    users_service = get_users_service()
    users_handlers = UsersBotHandlers(users_service)

    bank_service = get_bank_service()
    bank_handlers = BankBotHandlers(bank_service)

    app.add_handler(CommandHandler("start", users_handlers.start))
    app.add_handler(CommandHandler("set_phone", users_handlers.set_phone))
    app.add_handler(CommandHandler("me", users_handlers.get_info))
    app.add_handler(CommandHandler("card_balance", bank_handlers.get_card_balance))
    app.add_handler(CommandHandler("checking_account_balance", bank_handlers.get_checking_account_balance))
    app.add_handler(CommandHandler("transfer", bank_handlers.transfer_money_by_checking_account))
    app.add_handler(CommandHandler("transfer_name", bank_handlers.transfer_money_by_name))
    app.add_handler(CommandHandler("add_favorite", users_handlers.add_favorite_user))
    app.add_handler(CommandHandler("delete_favorite", users_handlers.delete_favorite_user))
    app.add_handler(CommandHandler("favorites", users_handlers.get_favorite_users))
    app.add_handler(CommandHandler("statement", bank_handlers.get_account_statement))
    app.add_handler(CommandHandler("interacted", bank_handlers.get_users_interacted_with))
    app.add_handler(CommandHandler("set_password", users_handlers.set_password))
    app.add_handler(CommandHandler("get_new_transactions", bank_handlers.get_new_transactions))

    app.add_handler(MessageHandler(filters.PHOTO, bank_handlers.transfer_by_account_with_image))



    app.run_polling()

    # app.run_webhook(
    #     listen="0.0.0.0",
    #     port=8000,
    #     webhook_url="https://adalarf.backend24.2tapp.cc/bot",
    #     url_path="bot"
    # )
