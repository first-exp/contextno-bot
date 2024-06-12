from aiogram.types import Message

from bot.services.challenge_service import ChallengeService


async def get_five_handle(message: Message, challenge_service: ChallengeService):
    await challenge_service.get_five_closest(message)
