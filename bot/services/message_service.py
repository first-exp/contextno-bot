from aiogram import Bot

from bot.keyboards.start_keyboard import startgame_inline


class MessageService:
    def __init__(self, bot: Bot):
        self.bot = bot

    async def send_rules(self, chat_id: int, rules: str):
        await self.bot.send_message(
            chat_id,
            f"<code>Основные правила</code>: {'\n'} <i>{rules}</i>",
            reply_markup=startgame_inline(),
        )
