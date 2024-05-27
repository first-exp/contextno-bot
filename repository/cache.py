from aioredis import Redis


WORD_RANK_KEY = "word_rank:{}"

class CacheRepository:
    def __init__(self, redis: Redis):
        self.redis = redis
        
    async def set_challenge_id_by_chat_id(self, chat_id: str, challenge_id: str):
         await self.redis.set(f"{chat_id}", challenge_id)
         
    async def get_challenge_id_by_chat_id(self, chat_id: str):
        await self.redis.get(f"{chat_id}")
        
    async def set_word_rank(self, chat_id: str, word: str, rank: int):
        key = WORD_RANK_KEY.format(chat_id)
        await self.redis.zadd(key, {word: rank}, nx=True)

    async def get_five_closests_words_by_chat_id(self, chat_id: str):
        key = WORD_RANK_KEY.format(chat_id)
        return await self.redis.zrange(key, 0, 4, withscores=True)
    
