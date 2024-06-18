from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.handles.get_five_handle import get_five_handle
from bot.handles.guess_word_handle import guess_word_handle
from bot.handles.new_game_handle import new_game_handle
from bot.handles.tip_handle import tip_handle
from bot.handles.welcome_instr_handle import hundle_welcome_instr
from bot.services.challenge_service import ChallengeService
from repository.contextno import ContextnoRepo

router = Router()


@router.message(CommandStart())
async def welcome_instructions(
    message: Message, state: FSMContext, challenge_service: ChallengeService
):
    await hundle_welcome_instr(message, state, challenge_service)


@router.message(Command("get"))
async def get_five(
    message: Message, repo: ContextnoRepo, challenge_service: ChallengeService
):
    await get_five_handle(message, challenge_service)


@router.message(Command("tip"))
async def get_help(message: Message, challenge_service: ChallengeService):
    await tip_handle(message, challenge_service)


@router.message(Command("new"))
async def new_game(message: Message, challenge_service: ChallengeService):
    await new_game_handle(message, challenge_service)


@router.message(F.text.lower())
async def guess_word(message: Message, challenge_service: ChallengeService):
    await guess_word_handle(message, challenge_service)
