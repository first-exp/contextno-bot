from aiogram import Bot, F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.handles.get_five_handle import get_five_handle
from bot.handles.guess_word_handle import guess_word_handle
from bot.handles.new_game_handle import new_game_handle
from bot.handles.tip_handle import tip_handle
from bot.handles.welcome_instr_handle import hundle_welcome_instr
from bot.services.challenge_service import ChallengeService
from bot.services.message_service import MessageService
from repository.cache import CacheRepository
from repository.contextno import ContextnoRepo

router = Router()


@router.message(CommandStart())
async def welcome_instructions(
    message: Message,
    state: FSMContext,
    repo: ContextnoRepo,
    cache: CacheRepository,
    bot: Bot,
):
    challenge_service = ChallengeService(repo, cache)
    message_service = MessageService(bot)

    await hundle_welcome_instr(message, state, challenge_service, message_service)


@router.message(Command("get"))
async def get_five(message: Message, repo: ContextnoRepo, cache: CacheRepository):
    challenge_service = ChallengeService(repo, cache)

    await get_five_handle(message, challenge_service)


@router.message(Command("tip"))
async def get_help(
    message: Message, repo: ContextnoRepo, cache: CacheRepository
) -> None:
    challenge_service = ChallengeService(repo, cache)

    await tip_handle(message, challenge_service)


@router.message(Command("new"))
async def new_game(message: Message, repo: ContextnoRepo, cache: CacheRepository):
    challenge_service = ChallengeService(repo, cache)

    await new_game_handle(message, challenge_service)


@router.message(F.text.lower())
async def guess_word(message: Message, repo: ContextnoRepo, cache: CacheRepository):
    challenge_service = ChallengeService(repo, cache)

    await guess_word_handle(message, challenge_service)
