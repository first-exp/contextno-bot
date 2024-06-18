from aiogram.types import Message

from bot.keyboards.start_keyboard import startgame_inline
from repository.cache import CacheRepository
from repository.contextno import ContextnoRepo

RULES = """\n- У тебя есть неограничнное количество попыток.\n
- Все слова в списке ранжированы по их схожести с секретным словом.\n
- Чем выше слово в списке (чем меньше его номер), тем оно ближе к секретному слову.\n"""


class ChallengeService:
    def __init__(self, repo: ContextnoRepo, cache: CacheRepository) -> None:
        self.repo = repo
        self.cache = cache

    async def set_challenge_id(self, chat_id: int):
        challenge_id = await self.repo.get_challenge_id(chat_id)
        await self.cache.set_challenge_id_by_chat_id(chat_id, str(challenge_id))

    async def get_challenge_id(self, chat_id: int):
        challenge_id = await self.cache.get_challenge_id_by_chat_id(chat_id)
        return challenge_id

    async def guess_word(
        self,
        challenge_id: int,
        message: Message,
    ):
        if message.text.count(" ") >= 1:
            await message.answer("<b>Ввведите слово, а не словосочетание</b>")
            return

        guess_word_model = await self.repo.get_word_rank(
            challenge_id, message.text.lower()
        )

        rank_icon = self.icons_for_ranks(guess_word_model.rank)

        if guess_word_model.error is True:
            await message.answer(
                "<i>"
                + guess_word_model.details.replace(
                    message.text.lower(), f"</i><b>{message.text.lower()}</b><i>"
                )
                + "</i>"
            )
        elif guess_word_model.rank == 1 and guess_word_model.completed is True:
            await message.answer(
                f"<i>Поздравляем! \n\nВы угадали слово</i> <b>{guess_word_model.word}</b> <i>за</i> {guess_word_model.tries} <i>попыток и</i> {guess_word_model.tips} <i>подсказок.</i> \n\n<i>Начать новую игру - <b>/new</b></i>"
            )
        else:
            await self.cache.set_word_rank(
                message.chat.id, message.text.lower(), guess_word_model.rank
            )
            await message.answer(
                f"{rank_icon} <b>{guess_word_model.word}</b> - <i>{guess_word_model.rank}</i>"
            )

    async def get_tip_response(self, challenge_id: int, message: Message):
        tip_word = await self.repo.get_tip(str(challenge_id))

        if tip_word.rank == 1:
            await message.answer(
                f"<i>Поздравляем! \n\nВы угадали слово</i> <b>{tip_word.word}</b> <i>за</i> {tip_word.tries} <i>попыток и</i> {tip_word.tips} <i>подсказок.</i> \n\n<i>Начать новую игру - <b>/new</b></i>"
            )
        elif tip_word.completed is True:
            await message.answer(
                'Вы уже отгадали слово. Нажмите /new для новой игры!'
            )
        elif tip_word.rank == -1:
            await message.answer("<b>Сначала введите слово</b>")
        else:
            await self.cache.set_word_rank(
                message.chat.id, tip_word.word, tip_word.rank
            )

            await message.answer(
                f"<i>Вот подсказка</i>: {self.icons_for_ranks(tip_word.rank)} <b>{tip_word.word}</b> - <i>{tip_word.rank}</i>"
            )

    async def get_five_closest(self, message: Message):
        five_closest = await self.cache.get_five_closests_words_by_chat_id(
            message.chat.id
        )
        if not five_closest:
            await message.answer("Нет данных о ближайших словах")
            return

        list_of_words = "\n".join(
            [
                f"{self.icons_for_ranks(rank)} <b>{word.decode('utf-8')}</b> - {int(rank)}"
                for word, rank in five_closest
            ]
        )

        await message.answer(list_of_words)

    async def send_rules(self, message: Message):
        await message.answer(
            f"<code>Основные правила</code>: \n <i>{RULES}</i>",
            reply_markup=startgame_inline(),
        )

    async def del_challenge_id(self, chat_id: int):
        await self.cache.delete_challenge_id_by_chat_id(chat_id)

    async def del_five_closest(self, chat_id: int):
        await self.cache.delete_word_ranks_by_chat_id(chat_id)

    def icons_for_ranks(self, rank: int):
        if rank >= 1500:
            return "🔴"
        elif rank > 300:
            return "🟡"
        else:
            return "🟢"
