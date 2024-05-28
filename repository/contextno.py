
from aiohttp import ClientSession
from models.contextno import Tip, WordRank


class ContextnoRepo:
    def __init__(self, http_session: ClientSession) -> None:
        self.http_session: ClientSession = http_session
        
    
    async def get_challenge_id(self, chat_id) -> int:
        resp = await self.http_session.get(
            url="https://xn--80aqu.xn--e1ajbkccewgd.xn--p1ai/get_random_challenge?user_id=contextno_bot"
            )
        sess_data = await resp.json()
        return int(sess_data['id'])


    async def get_word_rank(self, challenge_id, word) -> WordRank:
        url = ("https://xn--80aqu.xn--e1ajbkccewgd.xn--p1ai/get_score?"
            "challenge_id={}&user_id=contextno_bot&word={}&challenge_type=random")
        resp = await self.http_session.get(url.format(challenge_id, word))
        word_rank = WordRank(**await resp.json())
        return word_rank


    async def get_tip(self, challenge_id) -> Tip:
        url = ("https://xn--80aqu.xn--e1ajbkccewgd.xn--p1ai/get_tip?"
            "challenge_id={}&user_id=contextno_bot&challenge_type=random")
        resp = await self.http_session.get(url.format(challenge_id))
        tip = Tip(**await resp.json())
        return tip