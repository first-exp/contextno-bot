import asyncio
import logging
import sys

import redis
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiohttp import ClientSession

from bot.callbacks import start_game_callback
from bot.fsm import control_start_button
from bot.handlers import contextno_game
from bot.middlewares.repo_middleware import RepoMiddleware
from config_reader import config
from repository.cache import CacheRepository
from repository.contextno import ContextnoRepo


async def main():
    async with ClientSession() as session:
        bot = Bot(
            token=config.token_bot.get_secret_value(),
            default=DefaultBotProperties(parse_mode=ParseMode.HTML),
        )

        contextno_repo = ContextnoRepo(session)
        pool = redis.ConnectionPool.from_url("redis://localhost")
        cache_repo = CacheRepository(pool)

        dp = Dispatcher()

        dp.message.middleware(RepoMiddleware(contextno_repo, cache_repo))

        dp.include_routers(
            control_start_button.router,
            start_game_callback.router,
            contextno_game.router,
        )
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
