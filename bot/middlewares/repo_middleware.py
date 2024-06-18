from aiogram import BaseMiddleware
from aiogram.types import Message

from bot.services.challenge_service import ChallengeService
from repository.cache import CacheRepository
from repository.contextno import ContextnoRepo


class RepoMiddleware(BaseMiddleware):
    def __init__(
        self,
        repo: ContextnoRepo,
        cache: CacheRepository,
        challenge_service: ChallengeService,
    ):
        self.repo = repo
        self.cache = cache
        self.challenge_service = challenge_service

    async def __call__(self, handler, event: Message, data: dict):
        data["repo"] = self.repo
        data["cache"] = self.cache
        data["challenge_service"] = self.challenge_service

        return await handler(event, data)
