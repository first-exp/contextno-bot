from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.rules_and_secondary_func.rules_text import rules
from bot.services.challenge_service import ChallengeService
from bot.services.message_service import MessageService
from bot.states.start_button_state import Form


async def hundle_welcome_instr(
    message: Message,
    state: FSMContext,
    challenge_service: ChallengeService,
    message_service: MessageService,
):
    await challenge_service.set_challenge_id(message.chat.id)

    await message_service.send_rules(message.chat.id, rules)

    await state.set_state(Form.start_game_button.state)
