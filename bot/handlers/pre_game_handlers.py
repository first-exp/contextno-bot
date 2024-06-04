from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message

from repository.contextno import ContextnoRepo

# from repository.cache import CacheRepository
from keyboards.start_keyboard import startgame_inline
from text_rules.rules_text import rules
from aiogram.fsm.context import FSMContext
from states.start_button_state import Form

router = Router()


# @router.message(CommandStart())
# async def welcome_instructions(message: Message, state: FSMContext, repo: ContextnoRepo):
#     challenge_id = repo.get_challenge_id(chat_id=str(message.chat.id))
#     await message.answer(
#         f"<code>Основные правила</code>: {'\n'} <i>{rules}</i>",
#         reply_markup=startgame_inline(),
#         parse_mode="HTML",
#     )
#     await state.set_state(Form.start_game_button.state)


@router.message(CommandStart())
async def welcome_instructions(message: Message, state: FSMContext):
    await message.answer(
        f"<code>Основные правила</code>: {'\n'} <i>{rules}</i>",
        reply_markup=startgame_inline()
    )
    await state.set_state(Form.start_game_button.state)


@router.message(Form.start_game_button)
async def start_button_control(message: Message, state: FSMContext):
    data = await state.get_data()
    messages = data.get("messages", [])
    messages.append(message.message_id)
    await state.update_data(messages=messages)
    sent_message = await message.answer(
        "Пожалуйста, нажмите кнопку '<b>Понятно. К игре!</b>', чтобы продолжить."
    )
    messages.append(sent_message.message_id)
    await state.update_data(messages=messages)
