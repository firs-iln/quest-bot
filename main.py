import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from bot import router as quest_router
from config import config

TOKEN = config.TOKEN.get_secret_value()


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    dp = Dispatcher()

    dp.include_router(quest_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    while True:
        try:
            asyncio.run(main())
        except Exception as e:
            with open('crashes.txt', 'at', encoding='utf-8') as file:
                print(e, file=file)
