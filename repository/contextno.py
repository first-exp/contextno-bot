from aiohttp import ClientSession

from models.contextno import Tip, WordRank


class ContextnoRepo:
    def __init__(self, http_session: ClientSession) -> None:
        self.http_session = http_session
        self.url = "https://xn--80aqu.xn--e1ajbkccewgd.xn--p1ai"

    async def get_challenge_id(self, chat_id: int) -> str:
        url = self.url + "/get_random_challenge"
        params = {"user_id": "contextno_bot"}
        async with self.http_session.get(url=url, params=params) as resp:
            sess_data = await resp.json()
            return sess_data["id"]

    async def get_word_rank(self, challenge_id: int, word: str) -> WordRank:
        params = {
            "challenge_id": challenge_id,
            "word": word,
            "user_id": "contextno_bot",
            "challenge_type": "random",
        }
        url = self.url + "/get_score"
        async with self.http_session.get(url, params=params) as resp:
            word_rank = WordRank(**await resp.json())
            return word_rank

    async def get_tip(self, challenge_id: str) -> Tip:
        params = {
            "challenge_id": challenge_id,
            "user_id": "contextno_bot",
            "challenge_type": "random",
        }
        url = self.url + "/get_tip"
        async with self.http_session.get(url, params=params) as resp:
            tip = Tip(**await resp.json())
            return tip
