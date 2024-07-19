import time

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.states import QuestState
from core.QuestProcess import main_quest
from core.UserService import get_user_service
from core.schemas import UserCreate
from db.exceptions import NotFoundException

from logging import getLogger, FileHandler, addLevelName, CRITICAL

router = Router()

addLevelName(
    level=50,
    levelName='Winner',
)

winning_logger = getLogger('winning-logger')
winning_logger.addHandler(
    hdlr=FileHandler(
        filename='winners.txt'
    )
)

winning_logger.setLevel(CRITICAL)


@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    user = UserCreate(
        telegram_id=message.from_user.id,
        username=message.from_user.username,
    )
    async with get_user_service() as user_service:
        try:
            await user_service.get_user(telegram_id=message.from_user.id)
        except NotFoundException:
            await user_service.create_user(user)
            await message.answer(main_quest.start_message)
            await message.answer(main_quest.get_question(1))
            await state.set_state(QuestState.FIRST_QUESTION_ASKED)
        else:
            await message.answer("You've already started or completed the quest")


@router.message(QuestState.FIRST_QUESTION_ASKED)
async def second_question(message: Message, state: FSMContext):
    if not main_quest.check_answer(1, message.text):
        await message.answer("wrong answer")
        return

    await message.answer("First answer is right! Here's the second one:")
    await message.answer(main_quest.get_question(2))
    await state.set_state(QuestState.SECOND_QUESTION_ASKED)


@router.message(QuestState.SECOND_QUESTION_ASKED)
async def third_question(message: Message, state: FSMContext):
    if not main_quest.check_answer(2, message.text):
        await message.answer("wrong answer")
        return

    await message.answer("Second answer is right! Let's go deeper:")
    await message.answer(main_quest.get_question(3))
    await state.set_state(QuestState.THIRD_QUESTION_ASKED)


@router.message(QuestState.THIRD_QUESTION_ASKED)
async def fourth_question(message: Message, state: FSMContext):
    if not main_quest.check_answer(3, message.text):
        await message.answer("wrong answer")
        return

    await message.answer("Good for you! Could you deal with the next question?")
    await message.answer(main_quest.get_question(4))
    await state.set_state(QuestState.FOURTH_QUESTION_ASKED)


@router.message(QuestState.FOURTH_QUESTION_ASKED)
async def fourth_question(message: Message, state: FSMContext):
    if not main_quest.check_answer(4, message.text):
        await message.answer("wrong answer")
        return

    await message.answer("Fourth answer is right!")
    async with get_user_service() as user_service:
        await user_service.user_completed_quest(telegram_id=message.from_user.id)
        prizable = await user_service.check_if_user_prizable(telegram_id=message.from_user.id)
        position = await user_service.get_winners_position(telegram_id=message.from_user.id)
        if prizable:
            prize = await user_service.get_winners_prize(telegram_id=message.from_user.id)
            answer = main_quest.get_good_final(position=position, reward=prize)
            await state.set_state(QuestState.ASKED_FOR_WALLET)
            winning_logger.log(
                level=50,
                msg=f'{time.time()} - user {message.from_user.id} just won the {prize} prize!',
            )
        else:
            answer = main_quest.get_bad_final(position=position)
            await state.clear()

    await message.answer(answer)


@router.message(QuestState.ASKED_FOR_WALLET)
async def asked_for_wallet(message: Message, state: FSMContext):
    address = message.text
    async with get_user_service() as user_service:
        await user_service.set_wallet_address(telegram_id=message.from_user.id, wallet_address=address)

    await message.answer("Wallet address saved! You will receive your reward soon.")
    await state.clear()


@router.message()
async def already_completed(message: Message):
    await message.answer("You've already completed the quest!")
