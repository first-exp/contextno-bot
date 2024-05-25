# import os
# import datetime
from asyncio import Task, create_task, run

# import aiohttp 
from aiohttp import ClientResponse, ClientSession
from pydantic import BaseModel

# from aiogram import Bot, types, Dispatcher


class ContextnoSession(BaseModel):
    id: str
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
    challenge_id: str = new_cont_sess.id
    return challenge_id, my_http_session


async def get_word_rank(challenge_id, my_http_session, word):
    url = ("https://xn--80aqu.xn--e1ajbkccewgd.xn--p1ai/get_score?"
           "challenge_id={}&user_id=contextno_bot&word={}&challenge_type=random")
    resp: ClientResponse = await my_http_session.get(url.format(challenge_id, word))
    word_rank = WordRank(**await resp.json())
    print(word_rank)
    return word_rank


async def get_tip(challenge_id, my_http_session):
    url = ("https://xn--80aqu.xn--e1ajbkccewgd.xn--p1ai/get_tip?"
           "challenge_id={}&user_id=contextno_bot&challenge_type=random")
    resp: ClientResponse = await my_http_session.get(url.format(challenge_id))
    tip = Tip(**await resp.json())
    print(tip)
    return tip


async def main():
    task1: Task[tuple[str, ClientSession]] = create_task(start_session())
    challenge_id, my_http_session = await task1
    
    if challenge_id is not None:
        task2: Task[WordRank] = create_task(get_word_rank(
            my_http_session=my_http_session, challenge_id=challenge_id, word=word))
        await task2
        
        task3: Task[Tip] = create_task(get_tip(
            my_http_session=my_http_session, challenge_id=challenge_id))
        await task3
        
    
    await my_http_session.close()


if __name__ == "__main__":
    run(main=main())

# bot = Bot(token='your_bot_token')
# dp = Dispatcher(bot)
# @dp.message.handler(commands=["start"])
# async def start_game():
    
    
#     response = web.get(
#         path="https://xn--80aqu.xn--e1ajbkccewgd.xn--p1ai/get_random_challenge?user_id=contextno_bot",
#         handler=web.json_response()
#         )
#     # response = "smth"
#     print(response)
    
#     # await message.reply("получили сессию")
    
    
    
# if __name__ == "__main__":
#     asyncio.run(start_game())
    
	# С помощью метода executor.start_polling опрашиваем
     # Dispatcher: ожидаем команду /start
	# executor.start_polling(dp)