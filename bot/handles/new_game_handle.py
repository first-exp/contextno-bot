from aiogram.types import Message

from bot.services.challenge_service import ChallengeService


async def new_game_handle(message: Message, challenge_service: ChallengeService):
    await challenge_service.clear_caсhe()

    await challenge_service.set_challenge_id(message.chat.id)

    await message.answer("<b>Новая игра запущена...</b>")
