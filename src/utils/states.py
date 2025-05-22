from aiogram.fsm.state import StatesGroup, State


class ListStates(StatesGroup):
    CREATE_LIST_NAMING = State()
    UPDATE_LIST_NAMING = State()
    ADD_ITEMS_TO_LIST = State()
    ASSIGN_LIST = State()


class RegistrationStates(StatesGroup):
    PASSWORD_TYPING = State()
