from aiogram.types import Message

from bot.rules_and_secondary_func.get_five_func import get_five_response
from bot.rules_and_secondary_func.get_tip_check import get_tip_response
from bot.rules_and_secondary_func.guess_word_check import response_guess_word
from repository.cache import CacheRepository
from repository.contextno import ContextnoRepo


class ChallengeService:
    def __init__(self, repo: ContextnoRepo, cache: CacheRepository) -> None:
        self.repo = repo
        self.cache = cache

    async def set_challenge_id(self, chat_id: int):
        challenge_id = await self.repo.get_challenge_id(chat_id)
        await self.cache.set_challenge_id_by_chat_id(chat_id, str(challenge_id))

    async def get_challenge_id(self, chat_id: int):
        challenge_id = await self.cache.get_challenge_id_by_chat_id(chat_id)
        return challenge_id

    async def guess_word(self, challenge_id: int, message: Message):
        await response_guess_word(challenge_id, message, self.repo, self.cache)

    async def get_tip_word(self, challenge_id: int, message: Message):
        await get_tip_response(challenge_id, message, self.repo, self.cache)

    async def get_five_closest(self, message: Message):
        await get_five_response(message, self.cache)

    async def clear_caсhe(self):
        await self.cache.clear_db()
