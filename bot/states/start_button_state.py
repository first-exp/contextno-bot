from aiogram.fsm.state import StatesGroup, State

class Form(StatesGroup):
    start_game_button = State()