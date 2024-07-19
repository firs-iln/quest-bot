from aiogram.fsm.state import StatesGroup, State


class QuestState(StatesGroup):
    FIRST_QUESTION_ASKED = State()
    SECOND_QUESTION_ASKED = State()
    THIRD_QUESTION_ASKED = State()
    FOURTH_QUESTION_ASKED = State()
    ASKED_FOR_WALLET = State()
    ALL_QUESTIONS_ANSWERED = State()
