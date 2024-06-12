from aiogram.types import Message

from bot.rules_and_secondary_func.icons import icons_for_ranks
from repository.cache import CacheRepository


async def get_five_response(message: Message, cache: CacheRepository):
    five_closest = await cache.get_five_closests_words_by_chat_id(message.chat.id)
    if not five_closest:
        await message.answer("Нет данных о ближайших словах")
        return

    list_of_words = "\n".join(
        [
            f"{icons_for_ranks(rank)} <b>{word.decode('utf-8')}</b> - {int(rank)}"
            for word, rank in five_closest
        ]
    )

    await message.answer(list_of_words)
