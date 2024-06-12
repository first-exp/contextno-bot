from redis import ConnectionPool, Redis

WORD_RANK_KEY = "word_rank:{}"


class CacheRepository:
    def __init__(self, pool: ConnectionPool):
        self.pool = pool

    async def set_challenge_id_by_chat_id(self, chat_id: int, challenge_id: str):
        with Redis.from_pool(self.pool) as redis:
            redis.set(str(chat_id), challenge_id)

    async def get_challenge_id_by_chat_id(self, chat_id: int):
        with Redis.from_pool(self.pool) as redis:
            data = redis.get(str(chat_id))
            return data.decode("utf-8")

    async def set_word_rank(self, chat_id: int, word: str, rank: int):
        with Redis.from_pool(self.pool) as redis:
            key = WORD_RANK_KEY.format(chat_id)
            return redis.zadd(str(key), {word: rank}, nx=True)

    async def get_five_closests_words_by_chat_id(self, chat_id: int):
        with Redis.from_pool(self.pool) as redis:
            key = WORD_RANK_KEY.format(chat_id)
            return redis.zrange(str(key), 0, 4, withscores=True)

    async def clear_db(self):
        with Redis.from_pool(self.pool) as redis:
            return redis.flushdb()
