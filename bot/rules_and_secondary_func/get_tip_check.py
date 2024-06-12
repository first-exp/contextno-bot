from aiogram.types import Message

from bot.rules_and_secondary_func.icons import icons_for_ranks
from repository.cache import CacheRepository
from repository.contextno import ContextnoRepo


async def get_tip_response(
    challenge_id: int, message: Message, repo: ContextnoRepo, cache: CacheRepository
):
    tip_word = await repo.get_tip(str(challenge_id))

    if tip_word.rank == 1:
        await message.answer(
            f"<i>Поздравляем! \nВы угадали слово</i> <b>{tip_word.word}</b> <i>за</i> {tip_word.tries} <i>попыток и</i> {tip_word.tips} <i>подсказок.</i> \n\n<i>Начать новую игру - <b>/new</b></i>"
        )
    elif tip_word.rank == -1:
        await message.answer("<b>Сначала введите слово</b>")
    else:
        await cache.set_word_rank(message.chat.id, tip_word.word, tip_word.rank)

        await message.answer(
            f"<i>Вот подсказка</i>: {icons_for_ranks(tip_word.rank)} <b>{tip_word.word}</b> - <i>{tip_word.rank}</i>"
        )
