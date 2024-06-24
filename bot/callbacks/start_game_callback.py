from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

router = Router()


@router.callback_query(F.data == "start_game")
async def start_game(callback: CallbackQuery, bot: Bot, state: FSMContext):
    await callback.answer("Происходит магия...")
    data = await state.get_data()
    messages = data.get("messages", [])

    for message_id in messages:
        await bot.delete_message(callback.message.chat.id, message_id)

    await state.clear()
    await callback.message.edit_text("<b>Вы в игре...</b>")
