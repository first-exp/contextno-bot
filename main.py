import asyncio

from aiogram import Bot, Dispatcher, types
from config import token

bot = Bot(token=token)
dp = Dispatcher()


@dp.message()
async def any_text(message: types.Message):
    await message.answer("Hello!")


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())