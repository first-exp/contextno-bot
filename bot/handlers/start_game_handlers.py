import asyncio

from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext


# from filters.startgame_check import StartButtonCheck


router = Router()


@router.callback_query(F.data == 'start_game')
async def start_game(callback: CallbackQuery, bot: Bot, state: FSMContext):
    await callback.answer("Переход к игре...")
    await asyncio.sleep(1)
    data = await state.get_data()
    messages = data.get("messages", [])

    for message_id in messages:
        await bot.delete_message(callback.message.chat.id, message_id)

    await state.clear()
    await callback.message.edit_text("<b>Вы в игре...</b>")
    
    



