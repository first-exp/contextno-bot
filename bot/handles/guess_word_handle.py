from aiogram.types import Message

from bot.services.challenge_service import ChallengeService


async def guess_word_handle(message: Message, challenge_service: ChallengeService):
    challenge_id = await challenge_service.get_challenge_id(message.chat.id)
    await challenge_service.guess_word(challenge_id, message)
