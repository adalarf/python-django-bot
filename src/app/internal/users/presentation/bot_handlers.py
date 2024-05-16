from app.internal.users.domain.messages import UsersMessage
from app.internal.auth.domain.messages import AuthMessage
from app.internal.users.domain.service import UsersService
from telegram import Update
from telegram.ext import CallbackContext


class UsersBotHandlers:
    def __init__(self, users_service: UsersService):
        self._users_service = users_service

    async def start(self, update: Update, context: CallbackContext) -> None:
        user = update.effective_user
        await self._users_service.update_or_create_user(user.id, user.first_name)
        await update.message.reply_text(UsersMessage.name_added_to_db_message(user))

    async def set_phone(self, update: Update, context: CallbackContext) -> None:
        user = await self._users_service.get_user(update.effective_user.id)
        if len(context.args) == 0:
            await update.message.reply_text(UsersMessage.incorrect_phone_format_message())
            return
        phone_number = context.args[0]
        if not self._users_service.validate_phone(phone_number):
            await update.message.reply_text(UsersMessage.incorrect_phone_format_message())
        elif user.phone_number != phone_number:
            await self._users_service.set_phone_from_user(user, phone_number)
            await update.message.reply_text(UsersMessage.phone_added_to_db_message(user))
        else:
            await update.message.reply_text(UsersMessage.phone_already_added_to_db_message())

    async def get_info(self, update: Update, context: CallbackContext) -> None:
        user_info = await self._users_service.get_user_info(update.effective_user.id)
        await update.message.reply_text(user_info)

    async def set_password(self, update: Update, context: CallbackContext) -> None:
        if len(context.args) != 1:
            await update.message.reply_text(AuthMessage.password_not_provided_message())
            return
        password = context.args[0]
        user = update.effective_user.id
        await self._users_service.set_user_password(user, password)
        await update.message.reply_text(AuthMessage.password_is_set_message())

    async def add_favorite_user(self, update: Update, context: CallbackContext):
        user = update.effective_user
        favorite_name = context.args[0]
        if await self._users_service.add_user_to_favorite_list(user.id, favorite_name)\
                != UsersMessage.user_not_found_message():
            await update.message.reply_text(UsersMessage.added_favorite_user_message())
        else:
            await update.message.reply_text(UsersMessage.user_not_found_message())

    async def delete_favorite_user(self, update: Update, context: CallbackContext) -> None:
        user = update.effective_user
        favorite_name = context.args[0]
        if await self._users_service.delete_user_from_favorite_list(user.id, favorite_name)\
                != UsersMessage.user_not_found_message():
            await update.message.reply_text(UsersMessage.deleted_favorite_user_message())
        else:
            await update.message.reply_text(UsersMessage.user_not_found_message())

    async def get_favorite_users(self, update: Update, context: CallbackContext) -> None:
        user = update.effective_user
        favorites = await self._users_service.get_favorite_users_list(user.id)
        if favorites == UsersMessage.none_favorites_message():
            await update.message.reply_text(favorites)
        else:
            message = ""
            async for favorite in favorites:
                message += f"{favorite.name}"
            await update.message.reply_text(message)
