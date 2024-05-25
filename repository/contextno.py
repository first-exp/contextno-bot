# import os
# import datetime
from asyncio import Task, create_task, run

# import aiohttp 
from aiohttp import ClientResponse, ClientSession
from pydantic import BaseModel

# from aiogram import Bot, types, Dispatcher


class ContextnoSession(BaseModel):
    challenge_id: str = None  # type: ignore
    http_session: ClientSession
    chat_id: str = None  # type: ignore

class ContextnoSessionIn(ContextnoSession):
    id: str
    name: str

class WordRank(BaseModel):
    completed: bool
    details: str
    error: bool
    rank: int
    tips: int
    tries: int
    word: str


class Tip(WordRank):
    pass


word = "колбаса"
 
async def start_session():
    my_http_session = ClientSession()
    resp: ClientResponse = await my_http_session.get(
        url="https://xn--80aqu.xn--e1ajbkccewgd.xn--p1ai/get_random_challenge?user_id=contextno_bot"
        )
    new_cont_sess = ContextnoSessionIn(**await resp.json())
    game_session = ContextnoSession(challenge_id=new_cont_sess.id, http_session=my_http_session)
    return game_session


async def get_word_rank(game_session, word):
    url = ("https://xn--80aqu.xn--e1ajbkccewgd.xn--p1ai/get_score?"
           "challenge_id={}&user_id=contextno_bot&word={}&challenge_type=random")
    resp: ClientResponse = await game_session.http_session.get(url.format(game_session.challenge_id, word))
    word_rank = WordRank(**await resp.json())
    print(word_rank)
    return word_rank


async def get_tip(game_session):
    url = ("https://xn--80aqu.xn--e1ajbkccewgd.xn--p1ai/get_tip?"
           "challenge_id={}&user_id=contextno_bot&challenge_type=random")
    resp: ClientResponse = await game_session.http_session.get(url.format(game_session.challenge_id))
    tip = Tip(**await resp.json())
    print(tip)
    return tip


async def main():
    task1: Task[ContextnoSession] = create_task(start_session())
    game_session: ContextnoSession = await task1
    
    if game_session.challenge_id is not None:
                
        task2: Task[WordRank] = create_task(get_word_rank(
            game_session=game_session, word=word))
        await task2
        
        task3: Task[Tip] = create_task(get_tip(
            game_session))
        await task3
        
    
    await game_session.http_session.close()


if __name__ == "__main__":
    run(main=main())
