import asyncio
import logging
import sys
from datetime import datetime

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot import router as quest_router
from config import config

TOKEN = config.TOKEN.get_secret_value()
logger = logging.getLogger(__name__)


def increase_quest_step():
    config.QUEST_STEP += 1
    logger.info(config.QUEST_STEP)


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    dp = Dispatcher()

    dp.include_router(quest_router)

    scheduler = AsyncIOScheduler()

    logger.info(datetime.now())

    for i in range(2):
        scheduler.add_job(
            increase_quest_step,
            trigger="date",

            # TODO: replace time
            next_run_time=datetime.strptime(f"{28 + i}.08.2024 10:05", "%d.%m.%Y %H:%M"),
            max_instances=1,
        )

    scheduler.start()

    await dp.start_polling(bot)

    logger.info("shutdown")
    scheduler.shutdown()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    while True:
        try:
            asyncio.run(main())
        except Exception as e:
            with open('crashes.txt', 'at', encoding='utf-8') as file:
                print(e, file=file)
