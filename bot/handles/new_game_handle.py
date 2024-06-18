from aiogram.types import Message

from bot.services.challenge_service import ChallengeService


async def new_game_handle(message: Message, challenge_service: ChallengeService):
    await challenge_service.del_challenge_id(message.chat.id)

    await challenge_service.del_five_closest(message.chat.id)

    await challenge_service.set_challenge_id(message.chat.id)

    await message.answer("<b>Новая игра запущена...</b>")
