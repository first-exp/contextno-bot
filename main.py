import asyncio

from aiogram import Bot, Dispatcher, types
from config import get_settings

bot = Bot(token=get_settings().tg_token)
dp = Dispatcher()

# TODO: убрать этот хэндлер и диспетчер из этого файла после подключения сервисов
@dp.message()
async def any_text(message: types.Message):
    await message.answer("Hello!")


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

    