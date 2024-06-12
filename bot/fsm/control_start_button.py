from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.states.start_button_state import Form

router = Router()


@router.message(Form.start_game_button)
async def start_button_control(message: Message, state: FSMContext):
    data = await state.get_data()
    messages = data.get("messages", [])
    messages.append(message.message_id)
    await state.update_data(messages=messages)
    sent_message = await message.answer(
        "<i>Пожалуйста, нажмите кнопку</i> '<b>Понятно. К игре!</b>', <i>чтобы продолжить.</i>"
    )
    messages.append(sent_message.message_id)
    await state.update_data(messages=messages)
