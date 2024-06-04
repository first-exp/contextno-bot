from aiogram import Router, F
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

from repository.contextno import ContextnoRepo

# from models.contextno import WordRank

# from filters.correct_word import CorrectWordCheck

router = Router()


# @router.message(F.text)
# async def guess_word(message: Message, repo: ContextnoRepo):
#     guess_word_rank = await repo.get_word_rank(message.chat.id, message.text)

#     if guess_word_rank.rank > 1500:
#         await message.answer(f"🔴 {guess_word_rank.word} - {guess_word_rank.rank}")
#     elif 300 < word_rank.rank <= 1500:
#         await message.answer(f"🟡 {guess_word_rank.word} - {guess_word_rank.rank}")
#     else:
#         await message.answer(f"🟢 {guess_word_rank.word} - {guess_word_rank.rank}")


@router.message(Command("k"), F.text.count(" ") == 1)
async def guess_word(message: Message) -> None:
    await message.answer("Это слово")


@router.message(Command("k"), F.text.count(" ") > 1)
async def wrong_guess_word(message: Message) -> None:
    await message.answer("Введите слово, а не словосочетание")


# @router.message(Command('tip'))
# async def get_help(message: Message, repo: ContextnoRepo) -> None:
#     tip_command = await repo.get_tip(str(message.chat.id))

#     tip_model = Tip(**tip_command)

#     await message.answer()
