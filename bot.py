import asyncio
import logging


from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from aiogram.fsm.storage.memory import MemoryStorage
from config import DEBUG_MODE, TELEGRAM_TOKEN
from handlers import router
from scheduler import main as scheduler_main

from database import init_db


logger = logging.getLogger(__name__)


async def main():

    #set logging level
    if DEBUG_MODE:
        logging_level = logging.DEBUG
    else:
        logging_level = logging.INFO
    logging.basicConfig(
        level=logging_level,
        format="%(filename)s:%(lineno)d #%(levelname)-8s "
        "[%(asctime)s] - %(name)s - %(message)s",
    )

    logger.info("Starting SleepWell TG bot...")

    # Ensure the database is initialized
    init_db()

    bot: Bot = Bot(token=TELEGRAM_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
    storage = MemoryStorage()
    dp: Dispatcher = Dispatcher(storage=storage)
    dp.include_router(router)

    # Start the scheduler
    asyncio.create_task(scheduler_main())

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped.")
