from aiogram import BaseMiddleware
from aiogram.types import Message
from repository.cache import CacheRepository
from repository.contextno import ContextnoRepo

class RepoMiddleware(BaseMiddleware):
    def __init__(self, repo: ContextnoRepo, cache: CacheRepository):
        self.repo = repo
        self.cache = cache

    async def __call__(self, handler, event: Message, data: dict):
        data['repo'] = self.repo
        data['cache'] = self.cache
        return await handler(event, data)