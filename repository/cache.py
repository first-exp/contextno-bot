import aioredis


class CacheRepository:
    def __init__(self, redis_url: str):
        self.redis = aioredis.from_url(redis_url, decode_responses=True)
        self.word_rank_key = "word_rank:{}"
        
    async def set_challenge_id_by_chat_id(self, chat_id: str, challenge_id: str):
         await self.redis.set(f"challenge_id:{chat_id}", challenge_id)
         
    async def get_challenge_id_by_chat_id(self, chat_id: str):
        await self.redis.get(f"challenge_id:{chat_id}")
        
    async def set_word_rank(self, chat_id: str, word: str, rank: int):
        key = self.word_rank_key.format(chat_id)
        await self.redis.zadd(key, {word: rank}, nx=True)

    async def get_five_closests_words_by_chat_id(self, chat_id: str):
        key = self.word_rank_key.format(chat_id)
        return await self.redis.zrange(key, 0, 4, withscores=True)