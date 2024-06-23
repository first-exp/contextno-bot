from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.services.challenge_service import ChallengeService

router = Router()


@router.message(CommandStart())
async def welcome_instructions(
    message: Message, state: FSMContext, challenge_service: ChallengeService
):
    rules, markup = await challenge_service.send_rules(message, state)
    await message.answer(rules, reply_markup=markup)
    await challenge_service.start_new_game(message.chat.id)


@router.message(Command("get"))
async def get_five(message: Message, challenge_service: ChallengeService):
    five_closest_words = await challenge_service.get_five_closest(message)
    if not five_closest_words:
        await message.answer("<b>Нет данных о ближайших словах</b>")
        return
    await message.answer(five_closest_words)


@router.message(Command("tip"))
async def get_tip(message: Message, challenge_service: ChallengeService):
    tip_response = await challenge_service.get_tip_response(message)
    await message.answer(tip_response)


@router.message(Command("new"))
async def new_game(message: Message, challenge_service: ChallengeService):
    await challenge_service.start_new_game(message.chat.id)
    await message.answer("<b>Новая игра запущена...</b>")


@router.message(F.text.lower())
async def guess_word(message: Message, challenge_service: ChallengeService):
    if not message.text:
        await message.answer("<b>Введите слово!</b>")
        return

    if message.text.count(" ") >= 1:
        await message.answer("<b>Ввведите слово, а не словосочетание</b>")
        return

    text_response = await challenge_service.guess_word(
        message.chat.id, message.text.lower()
    )
    await message.answer(text_response)
