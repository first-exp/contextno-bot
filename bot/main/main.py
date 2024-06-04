import asyncio
import logging
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from aiohttp import ClientSession
from middlewares.throttlingware import ThrottlingMiddleware
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from config_reader import config
from aiogram.enums import ParseMode
from handlers import start_game_handlers, pre_game_handlers, contextno_game
from repository.contextno import ContextnoRepo


async def main():
    bot = Bot(
        token=config.token_bot.get_secret_value(),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()

    dp.message.middleware(ThrottlingMiddleware())

    dp.include_routers(
        pre_game_handlers.router, start_game_handlers.router, contextno_game.router
    )
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
