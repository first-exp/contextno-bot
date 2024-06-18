from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.services.challenge_service import ChallengeService
from bot.states.start_button_state import Form
from repository.contextno import ContextnoRepo

router = Router()


@router.message(CommandStart())
async def welcome_instructions(
    message: Message, state: FSMContext, challenge_service: ChallengeService
):
    # TODO: Тут тоже дергаешь репозиторий, такого не должно быть.
    # нужно вынести в метод сервиса get_tip 
    await challenge_service.set_challenge_id(message.chat.id)
    await challenge_service.send_rules(message)
    if message.chat.type == "private":
        await state.set_state(Form.start_game_button.state)


@router.message(Command("get"))
async def get_five(
    message: Message, repo: ContextnoRepo, challenge_service: ChallengeService
):
    # Вот тут ты правильно сделал, что все убрал в один метод сервиса. Я немного поправил его, чтобы он возвращал строку, а не отправлял сообщение.
    # можешь использовать как пример для других методов.
    five_closest_words = await challenge_service.get_five_closest(message)
    if not five_closest_words:
        await message.answer("Нет данных о ближайших словах")
        return
    await message.answer(five_closest_words)


@router.message(Command("tip"))
async def get_tip(message: Message, challenge_service: ChallengeService):
    # TODO: Тут тоже дергаешь репозиторий, такого не должно быть.
    # нужно вынести в метод сервиса get_tip 
    challenge_id = await challenge_service.get_challenge_id(message.chat.id)
    await challenge_service.get_tip_response(challenge_id, message)


@router.message(Command("new"))
async def new_game(message: Message, challenge_service: ChallengeService):
    # TODO: тут три раза вызываются репозитории.
    # Мы используем сервис не для того, чтобы через него вызвать репозитории, а чтобы скрыть в его методах логику работы, в том числе и с репозиториями.
    # Нужно создать в сервисе новый метот start_new_game и всю логику перенести в него.
    # Тут останется только вызов этого метода и отправка сообщения.
    # await challenge_service.start_new_game(...) и await message.answer("<b>Новая игра запущена...</b>")
    
    # Вот это вынести:
    await challenge_service.del_challenge_id(message.chat.id)
    await challenge_service.del_five_closest(message.chat.id)
    await challenge_service.set_challenge_id(message.chat.id)
    # ================================================================
    # await challenge_service.start_new_game(...)
    await message.answer("<b>Новая игра запущена...</b>")


@router.message(F.text.lower())
async def guess_word(message: Message, challenge_service: ChallengeService):
    # TODO: Тут тоже дергаешь репозиторий, такого не должно быть.
    # нужно вынести в метод сервиса guess_word
    challenge_id = await challenge_service.get_challenge_id(message.chat.id)
    await challenge_service.guess_word(challenge_id, message)
