# import os
# import datetime
from asyncio import Task, create_task, run

# import aiohttp 
from aiohttp import ClientResponse, ClientSession
from pydantic import BaseModel

# from aiogram import Bot, types, Dispatcher


class ContextnoSession(BaseModel):
    challenge_id: str
    chat_id: str = None  # type: ignore

class ContextnoSessionIn(BaseModel):
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
 
async def start_game(http_session):
    try:
        resp: ClientResponse = await http_session.get(
            url="https://xn--80aqu.xn--e1ajbkccewgd.xn--p1ai/get_random_challenge?user_id=contextno_bot"
            )
        new_cont_sess = ContextnoSessionIn(**await resp.json())
        game_sess = ContextnoSession(challenge_id=new_cont_sess.id)
    except Exception as e:
            print(f"Error starting session: {e}")
    return game_sess


async def get_word_rank(challenge_id, http_session, word):
    try:
        url = ("https://xn--80aqu.xn--e1ajbkccewgd.xn--p1ai/get_score?"
            "challenge_id={}&user_id=contextno_bot&word={}&challenge_type=random")
        resp: ClientResponse = await http_session.get(url.format(challenge_id, word))
        word_rank = WordRank(**await resp.json())
        print(word_rank)
    except Exception as e:
            print(f"Error get word rank: {e}")
    return word_rank


async def get_tip(challenge_id, http_session):
    try:
        url = ("https://xn--80aqu.xn--e1ajbkccewgd.xn--p1ai/get_tip?"
            "challenge_id={}&user_id=contextno_bot&challenge_type=random")
        resp: ClientResponse = await http_session.get(url.format(challenge_id))
        tip = Tip(**await resp.json())
        print(tip)
    except Exception as e:
        print(f"Error get tip: {e}")
    return tip


async def main():
    with ClientSession() as http_session:
        task1: Task[ContextnoSession] = create_task(start_game(http_session=http_session))
        game_sess: ContextnoSession = await task1
        
        if game_sess.challenge_id is not None:
            task2: Task[WordRank] = create_task(get_word_rank(
                http_session=http_session, challenge_id=game_sess.challenge_id, word=word))
            await task2
            
            task3: Task[Tip] = create_task(get_tip(
                http_session=http_session, challenge_id=game_sess.challenge_id))
            await task3
        

if __name__ == "__main__":
    run(main=main())

