
from aiohttp import ClientResponse
from models.contextno import ContextnoSession, ContextnoSessionIn, Tip, WordRank


class ContextnoRepo:
    def __init__(self, http_session):
        self.http_session = http_session
        
    
    async def start_game(self) -> ContextnoSession:
        try:
            resp: ClientResponse = await self.http_session.get(
                url="https://xn--80aqu.xn--e1ajbkccewgd.xn--p1ai/get_random_challenge?user_id=contextno_bot"
                )
            new_cont_sess = ContextnoSessionIn(**await resp.json())
            game_sess = ContextnoSession(challenge_id=new_cont_sess.id)
        except Exception as e:
                print(f"Error starting session: {e}")
        return game_sess


    async def get_word_rank(self, challenge_id, word) -> WordRank:
        try:
            url = ("https://xn--80aqu.xn--e1ajbkccewgd.xn--p1ai/get_score?"
                "challenge_id={}&user_id=contextno_bot&word={}&challenge_type=random")
            resp: ClientResponse = await self.http_session.get(url.format(challenge_id, word))
            word_rank = WordRank(**await resp.json())
        except Exception as e:
                print(f"Error get word rank: {e}")
        return word_rank


    async def get_tip(self, challenge_id) -> Tip:
        try:
            url = ("https://xn--80aqu.xn--e1ajbkccewgd.xn--p1ai/get_tip?"
                "challenge_id={}&user_id=contextno_bot&challenge_type=random")
            resp: ClientResponse = await self.http_session.get(url.format(challenge_id))
            tip = Tip(**await resp.json())
        except Exception as e:
            print(f"Error get tip: {e}")
        return tip