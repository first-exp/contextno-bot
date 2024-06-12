from aiogram.types import Message

from bot.rules_and_secondary_func.icons import icons_for_ranks
from repository.cache import CacheRepository
from repository.contextno import ContextnoRepo


async def response_guess_word(
    challenge_id: int, message: Message, repo: ContextnoRepo, cache: CacheRepository
):
    if message.text.count(" ") >= 1:
        await message.answer("<b>Ввведите слово, а не словосочетание</b>")
        return

    guess_word_model = await repo.get_word_rank(challenge_id, message.text.lower())

    rank_icon = icons_for_ranks(guess_word_model.rank)

    if guess_word_model.details.endswith("аре"):
        await message.answer(
            f"<i>Слово</i> <b>{message.text.lower()}</b> <i>не найдено в словаре</i>"
        )
    elif guess_word_model.details.endswith("ано"):
        await message.answer(
            f"<i>Слово</i> <b>{message.text.lower()}</b> <i>уже было использовано</i>"
        )
    elif guess_word_model.rank == 1:
        await message.answer(
            f"<i>Поздравляем! \nВы угадали слово</i> <b>{guess_word_model.word}</b> <i>за</i> {guess_word_model.tries} <i>попыток и</i> {guess_word_model.tips} <i>подсказок.</i> \n\n<i>Начать новую игру - <b>/new</b></i>"
        )
    else:
        await cache.set_word_rank(
            message.chat.id, message.text.lower(), guess_word_model.rank
        )

        await message.answer(
            f"{rank_icon} <b>{guess_word_model.word}</b> - <i>{guess_word_model.rank}</i>"
        )
