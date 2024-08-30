import time

from aiogram import Router, F, Bot
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from bot.states import QuestState
from config import config
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
            await message.answer(main_quest.get_question(1))
            await state.set_state(QuestState.FIRST_QUESTION_ASKED)
        else:
            await message.answer("You've already started or completed the quest")


@router.message(QuestState.FIRST_QUESTION_ASKED, lambda _: config.QUEST_STEP == 1)
async def check_first_question(message: Message, state: FSMContext):
    if not main_quest.check_answer(1, message.text):
        await message.answer("This answer is wrong")
        return

    if config.QUEST_STEP == 1:
        await message.answer("Thats the right answer! The second stage starts tomorrow, follow @yumify")
    else:
        await message.answer("That's right, move on!")
    async with get_user_service() as user_service:
        await user_service.passed_first_day(message.from_user.id)

    await state.set_state(QuestState.FIRST_QUESTION_CHECKED)


@router.message(QuestState.SECOND_QUESTION_ASKED, lambda _: config.QUEST_STEP == 2)
async def check_second_question(message: Message, state: FSMContext):
    if not main_quest.check_answer(2, message.text):
        await message.answer("This answer is wrong")
        return

    await message.answer("Right!")
    async with get_user_service() as user_service:
        await user_service.passed_second_day(user_id=message.from_user.id)

    await state.set_state(QuestState.SECOND_QUESTION_CHECKED)


# @router.message(lambda _: config.QUEST_STEP in [1, 2])
async def second_question(message: Message, state: FSMContext):
    if config.QUEST_STEP == 1:
        await message.answer("Be patient! The second stage starts tomorrow, follow @yumify")
        return

    await message.answer(main_quest.get_question(2))
    await state.set_state(QuestState.SECOND_QUESTION_ASKED)


# @router.message(lambda _: config.QUEST_STEP in [2, 3])
async def hi(message: Message, state: FSMContext):
    if config.QUEST_STEP == 2:
        await message.answer(
            "It's all for today! Come back tomorrow to take part in our quest (follow @yumify to stay informed)"
        )
        return

    await message.answer("We are pleased to welcome you to the second stage of the @yumify quest!"
                         "This time it will be more difficult and interesting! Good luck!")
    await message.answer("Send me your TON wallet")
    await state.set_state(QuestState.ASKED_FOR_WALLET)


@router.message(QuestState.ASKED_FOR_WALLET, lambda _: config.QUEST_STEP == 3)
async def ask_confirm_wallet(message: Message, state: FSMContext):
    wallet = message.text
    markup = InlineKeyboardMarkup(inline_keyboard=
    [
        [
            InlineKeyboardButton(text="Confirm?", callback_data=f"confirm_{wallet}"),
        ],

    ],
    )
    await message.answer(f"Your wallet is {wallet}?", reply_markup=markup)

    await state.set_state(QuestState.ASKED_FOR_WALLET_CONFIRM)


@router.callback_query(
    QuestState.ASKED_FOR_WALLET_CONFIRM,
    F.data.startswith("confirm"),
    lambda _: config.QUEST_STEP == 3
)
async def save_wallet(callback: CallbackQuery, state: FSMContext, bot: Bot):
    address = callback.data.replace("confirm_", "")
    async with get_user_service() as user_service:
        await user_service.set_wallet_address(telegram_id=callback.from_user.id, wallet_address=address)

    await callback.answer("Your wallet has been saved")

    await bot.send_message(chat_id=callback.from_user.id,
                           text="To participate in the quest, you need to publish a stories with this picture and text 'I play in @Yumify_Bot'\n"
                                "Send the link to your story to me. Do not delete it until our manager writes to you. "
                                "(Post a stories for 48 hours)")
    await bot.send_photo(chat_id=callback.from_user.id,
                         photo='AgACAgIAAxkBAAOCZtGpON53Ea_mqNfjdruKyOItS7UAAongMRsblpFK2mzN2bKe1vMBAAMCAANzAAM1BA')
    await state.set_state(QuestState.ASKED_FOR_LINK)


# @router.message(QuestState.ASKED_FOR_LINK)
# async def ask_story_link(message: Message, state: FSMContext):
#     await message.answer(
#         "To participate in the quest, you need to publish a stories with this picture and text 'I play in @Yumify_Bot'"
#         "Send the link to your story to me. Do not delete it until our manager writes to you."
#         "(Post a stories for 48 hours)")
#     await message.answer_photo(photo='AgACAgIAAxkBAANXZs22bQyyoCkAAXMrrRrV-L9uAzQwAAIL4DEbN_RwSoelmEeXXzwuAQADAgADcwADNQQ')
#     await state.set_state(QuestState.ASKED_FOR_LINK)


# @router.message()
# async def get_file_id(message: Message):
#     await message.answer(message.document.file_id)
#     # await message.answer(message.photo[0].file_id)


@router.message(QuestState.ASKED_FOR_LINK, lambda _: config.QUEST_STEP == 3)
async def save_story_link(message: Message, state: FSMContext):
    link = message.text
    # сохранить
    user_id = message.from_user.id
    async with get_user_service() as user_service:
        await user_service.add_story_link(user_id=user_id, story_link=link)

    markup = InlineKeyboardMarkup(inline_keyboard=
    [
        [
            InlineKeyboardButton(text="Ready?", callback_data="ready"),
        ],

    ],
    )
    await message.answer(
        "The link is saved! "
        "The quest will gradually become more difficult, and only the strongest will be able to complete it."
        "Ready to get started?", reply_markup=markup)

    await state.set_state(QuestState.SAVED_LINK)


@router.callback_query(QuestState.SAVED_LINK, F.data == "ready", lambda _: config.QUEST_STEP == 3)
async def third_question(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await bot.send_message(text=main_quest.get_question(3), chat_id=callback.from_user.id)
    await state.set_state(QuestState.THIRD_QUESTION_ASKED)


@router.message(QuestState.THIRD_QUESTION_ASKED, lambda _: config.QUEST_STEP == 3)
async def fourth_question(message: Message, state: FSMContext):
    if not main_quest.check_answer(3, message.text):
        await message.answer("This answer is wrong")
        return

    # await message.answer("Good for you! Could you deal with the next question?")
    await message.answer(main_quest.get_question(4))
    await state.set_state(QuestState.FOURTH_QUESTION_ASKED)


@router.message(QuestState.FOURTH_QUESTION_ASKED, lambda _: config.QUEST_STEP == 3)
async def fifth_question(message: Message, state: FSMContext):
    if not main_quest.check_answer(4, message.text):
        await message.answer("This answer is wrong")
        return

    await message.answer("Right!")
    await message.answer(main_quest.get_question(5))
    await state.set_state(QuestState.FIFTH_QUESTION_ASKED)


@router.message(QuestState.FIFTH_QUESTION_ASKED, lambda _: config.QUEST_STEP == 3)
async def sixth_question(message: Message, state: FSMContext):
    if not main_quest.check_answer(5, message.text):
        await message.answer("This answer is wrong")
        return

    await message.answer("This answer is right")
    await message.answer(main_quest.get_question(6))
    await state.set_state(QuestState.SIXTH_QUESTION_ASKED)


@router.message(QuestState.SIXTH_QUESTION_ASKED, lambda _: config.QUEST_STEP == 3)
async def seventh_question(message: Message, state: FSMContext):
    if not main_quest.check_answer(6, message.text):
        await message.answer("This answer is wrong")
        return

    await message.answer("Sure! Let's have a look at the next riddle")
    await message.answer(main_quest.get_question(7))
    await state.set_state(QuestState.SEVENTH_QUESTION_ASKED)


@router.message(QuestState.SEVENTH_QUESTION_ASKED, lambda _: config.QUEST_STEP == 3)
async def eighth_question(message: Message, state: FSMContext):
    if not main_quest.check_answer(7, message.text):
        await message.answer("This answer is wrong")
        return

    await message.answer("You're right!")
    await message.answer(main_quest.get_question(8))
    await state.set_state(QuestState.EIGHTH_QUESTION_ASKED)


@router.message(QuestState.EIGHTH_QUESTION_ASKED, lambda _: config.QUEST_STEP == 3)
async def ninth_question(message: Message, state: FSMContext):
    if not main_quest.check_answer(8, message.text):
        await message.answer("This answer is wrong")
        return

    await message.answer("Yes, that's right")
    await message.answer(main_quest.get_question(9))
    await message.answer_document(document="BQACAgIAAxkBAAOEZtGpfBjsCiiSZPIoroVg2gVx_LIAAsBPAAIblpFK3UfXXF7lArs1BA")
    await state.set_state(QuestState.NINTH_QUESTION_ASKED)


@router.message(QuestState.NINTH_QUESTION_ASKED, lambda _: config.QUEST_STEP == 3)
async def tenth_question(message: Message, state: FSMContext):
    if not main_quest.check_answer(9, message.text):
        await message.answer("This answer is wrong")
        return

    await message.answer("Cool, get ready for the next question!")
    await message.answer(main_quest.get_question(10))
    await state.set_state(QuestState.TENTH_QUESTION_ASKED)


@router.message(QuestState.TENTH_QUESTION_ASKED, lambda _: config.QUEST_STEP == 3)
async def eleventh_question(message: Message, state: FSMContext):
    if not main_quest.check_answer(10, message.text):
        await message.answer("This answer is wrong")
        return

    await message.answer("Good for you! Could you deal with the next question?")
    await message.answer(main_quest.get_question(11))
    await state.set_state(QuestState.ELEVENTH_QUESTION_ASKED)


@router.message(QuestState.ELEVENTH_QUESTION_ASKED, lambda _: config.QUEST_STEP == 3)
async def last_question_check(message: Message, state: FSMContext):
    if not main_quest.check_answer(11, message.text):
        await message.answer("This answer is wrong")
        return

    await message.answer("Answer is right!")
    async with get_user_service() as user_service:
        await user_service.user_completed_quest(telegram_id=message.from_user.id)
        prizable = await user_service.check_if_user_prizable(telegram_id=message.from_user.id)
        position = await user_service.get_winners_position(telegram_id=message.from_user.id)
        if prizable:
            prize = await user_service.get_winners_prize(telegram_id=message.from_user.id)
            answer = main_quest.get_good_final(position=position, reward=prize)
            winning_logger.critical(
                f'{time.time()} - user {message.from_user.id} just won the {prize} prize!',
            )
        else:
            answer = main_quest.get_bad_final()

    await message.answer(answer)
    await state.set_state(QuestState.ALL_QUESTIONS_ANSWERED)


@router.message(QuestState.ALL_QUESTIONS_ANSWERED)
async def already_completed(message: Message):
    await message.answer("You've already completed the quest!")


@router.message()
async def dispatch_user(message: Message, state: FSMContext):
    async with get_user_service() as user_service:
        try:
            user = await user_service.get_user(telegram_id=message.from_user.id)
        except NotFoundException:
            await start(message=message, state=state)
            return

        match config.QUEST_STEP:
            case 1:
                if user.passed_first_day:
                    await message.answer("Be patient! The second stage starts tomorrow, follow @yumify")
                else:
                    await start(message=message, state=state)
            case 2:
                if user.passed_second_day:
                    await message.answer(
                        "It's all for today! Come back tomorrow to take part in our quest (follow @yumify to stay informed)"
                    )
                else:
                    if user.passed_first_day:
                        await second_question(message=message, state=state)
                    else:
                        if await state.get_state() == QuestState.FIRST_QUESTION_ASKED:
                            await check_first_question(message=message, state=state)
                        else:
                            await start(message=message, state=state)
            case 3:
                if user.passed_first_day and user.passed_second_day:
                    await hi(message=message, state=state)
                elif user.passed_first_day and not user.passed_second_day:
                    if await state.get_state() == QuestState.SECOND_QUESTION_ASKED:
                        await check_second_question(message=message, state=state)
                    else:
                        await second_question(message=message, state=state)
                elif not user.passed_first_day and not user.passed_second_day:
                    if await state.get_state() == QuestState.FIRST_QUESTION_ASKED:
                        await check_first_question(message=message, state=state)
                    else:
                        await start(message=message, state=state)
            case _:
                raise NotImplementedError()
