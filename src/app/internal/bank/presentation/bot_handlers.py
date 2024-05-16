from app.internal.bank.domain.messages import BankMessage
from app.internal.bank.domain.service import BankService
from telegram import Update
from telegram.ext import CallbackContext


class BankBotHandlers:
    def __init__(self, bank_service: BankService):
        self._bank_service = bank_service

    async def get_card_balance(self, update: Update, context: CallbackContext) -> None:
        if len(context.args) == 0:
            await update.message.reply_text(BankMessage.card_incorrect_format_message())
            return
        card_number = context.args[0]
        if len(card_number) != 16:
            await update.message.reply_text(BankMessage.card_incorrect_length_message())
        else:
            card_balance = await self._bank_service.try_get_card_balance(card_number)
            await update.message.reply_text(card_balance)

    async def get_checking_account_balance(self, update: Update, context: CallbackContext) -> None:
        if len(context.args) == 0:
            await update.message.reply_text(BankMessage.checking_account_incorrect_format_message())
            return
        account_number = context.args[0]
        if len(account_number) != 20:
            await update.message.reply_text(BankMessage.checking_account_incorrect_length_message())
        else:
            checking_account = await self._bank_service.try_get_checking_account_balance(account_number)
            await update.message.reply_text(checking_account)

    async def transfer_money_by_name(self, update: Update, context: CallbackContext) -> None:
        favorite_name = context.args[0]
        favorite_accounts = await self._bank_service.transfer_by_name(favorite_name)
        await update.message.reply_text(favorite_accounts)

    async def transfer_money_by_checking_account(self, update: Update, context: CallbackContext) -> None:
        user_account = context.args[0]
        favorite_account = context.args[1]
        money_amount = context.args[2]

        if not update.message.photo:
            transfer = await self._bank_service.transfer_by_checking_account(user_account, favorite_account,
                                                                             money_amount)
        else:
            postcard_file = await context.bot.get_file(update.message.photo[-1].file_id)
            postcard_type = postcard_file.file_path.split(".")[-1]
            postcard = await postcard_file.download_as_bytearray()
            transfer = await self._bank_service.transfer_by_checking_account(user_account, favorite_account,
                                                                             money_amount, postcard, postcard_type)
        await update.message.reply_text(transfer)

    async def get_new_transactions(self, update: Update, context: CallbackContext) -> None:
        account_number = context.args[0]
        transactions = await self._bank_service.get_new_transactions(account_number)
        transactions = list(transactions)
        await update.message.reply_text(await BankMessage.get_new_transactions_message(transactions))

    async def transfer_by_account_with_image(self, update: Update, context: CallbackContext) -> None:
        if update.message.caption is None:
            return
        command_caption = update.message.caption.split()
        if command_caption[0] != "/transfer":
            return
        context.args = command_caption[1:]
        await self.transfer_money_by_checking_account(update, context)

    async def get_account_statement(self, update: Update, context: CallbackContext) -> None:
        checking_account = context.args[0]
        date_start = context.args[1]
        date_end = context.args[2]
        if date_start > date_end:
            await update.message.reply_text("Дата начала не может быть позже даты окончания")
            return
        statement = await self._bank_service.get_checking_account_statement(checking_account, date_start, date_end)
        statement = list(statement)
        await update.message.reply_text(BankMessage.statement_message(statement))

    async def get_users_interacted_with(self, update: Update, context: CallbackContext) -> None:
        checking_account = context.args[0]
        interacted_users = await self._bank_service.get_interacted_users(checking_account)
        interacted_users_list = list(interacted_users)
        await update.message.reply_text(BankMessage.interacted_users_message(interacted_users_list))
