from aiogram.fsm.state import State, StatesGroup


class Form(StatesGroup):
    start_game_button = State()
