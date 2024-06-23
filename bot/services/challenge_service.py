from aiogram.types import Message

from bot.keyboards.start_keyboard import startgame_inline
from bot.states.start_button_state import Form
from models.contextno import WordRank
from repository.cache import CacheRepository
from repository.contextno import ContextnoRepo

RULES = """\n- У тебя есть неограничнное количество попыток.\n
- Все слова в списке ранжированы по их схожести с секретным словом.\n
- Чем выше слово в списке (чем меньше его номер), тем оно ближе к секретному слову.\n"""


class NoMessageTextException(Exception):
    def __init__(self, message: Message):
        self.message = message
        super().__init__(f"Message {message} has no text")


class ChallengeService:
    def __init__(self, repo: ContextnoRepo, cache: CacheRepository) -> None:
        self.repo = repo
        self.cache = cache

    async def set_challenge_id(self, chat_id: int):
        challenge_id = await self.repo.get_challenge_id(chat_id)
        await self.cache.set_challenge_id_by_chat_id(chat_id, str(challenge_id))

    async def get_challenge_id(self, chat_id: int):
        return await self.cache.get_challenge_id_by_chat_id(chat_id)

    async def guess_word(self, chat_id: int, message_text: str) -> str:
        challenge_id = await self.get_challenge_id(chat_id)

        guess_word_model = await self.repo.get_word_rank(challenge_id, message_text)

        return await self.__prepare_answer_text_and_add_word_to_cache(
            message_text, guess_word_model, chat_id
        )

    async def get_tip_response(self, message: Message):
        challenge_id = await self.get_challenge_id(message.chat.id)
        tip_word = await self.repo.get_tip(str(challenge_id))

        return await self.__prepare_answer_text_and_add_word_to_cache(
            message.text, tip_word, message.chat.id
        )

    async def get_five_closest(self, message: Message) -> str | None:
        five_closest = await self.cache.get_five_closests_words_by_chat_id(
            message.chat.id
        )
        if not five_closest:
            return None

        return "\n".join(
            [
                f"{self.__icons_for_ranks(rank)} <b>{word.decode('utf-8')}</b> - {int(rank)}"
                for word, rank in five_closest
            ]
        )

    async def send_rules(self, message: Message, state) -> tuple:
        if message.chat.type == "private":
            await state.set_state(Form.start_game_button.state)
        return f"<code>Основные правила</code>: \n <i>{RULES}</i>", startgame_inline()

    async def start_new_game(self, chat_id: int):
        await self.cache.delete_challenge_id_by_chat_id(chat_id)
        await self.cache.delete_word_ranks_by_chat_id(chat_id)
        await self.set_challenge_id(chat_id)

    async def __prepare_answer_text_and_add_word_to_cache(
        self, message_text: str, guess_word_model: WordRank, chat_id: int
    ) -> str:
        if guess_word_model.error is True and guess_word_model.completed is True:
            return "<b>Игра закончена. Введите</b> /new <b>для новой игры</b>"
        elif guess_word_model.error is True and guess_word_model.word:
            return (
                "<i>"
                + guess_word_model.details.replace(
                    message_text, f"</i><b>{message_text}</b><i>"
                )
                + "</i>"
            )
        elif guess_word_model.rank == -1:
            return "<b>Сначала введите слово</b>"
        elif guess_word_model.rank == 1 and guess_word_model.completed is True:
            return f"<i>Поздравляем! \n\nВы угадали слово</i> <b>{guess_word_model.word}</b> <i>за</i> {guess_word_model.tries} <i>попыток и</i> {guess_word_model.tips} <i>подсказок.</i> \n\n<i>Начать новую игру - </i>/new"
        else:
            rank_icon = self.__icons_for_ranks(guess_word_model.rank)
            await self.cache.set_word_rank(
                chat_id, guess_word_model.word, guess_word_model.rank
            )
            return f"{rank_icon} <b>{guess_word_model.word}</b> - <i>{guess_word_model.rank}</i>"

    def __icons_for_ranks(self, rank: int):
        if rank >= 1500:
            return "🔴"
        elif rank > 300:
            return "🟡"
        else:
            return "🟢"
