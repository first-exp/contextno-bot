from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.services.challenge_service import ChallengeService
from bot.states.start_button_state import Form


async def hundle_welcome_instr(
    message: Message, state: FSMContext, challenge_service: ChallengeService
):
    if message.chat.type == "private":
        await challenge_service.set_challenge_id(message.chat.id)

        await challenge_service.send_rules(message)

        await state.set_state(Form.start_game_button.state)

    else:
        await challenge_service.set_challenge_id(message.chat.id)

        await challenge_service.send_rules(message)
