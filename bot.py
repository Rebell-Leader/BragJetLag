import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import TELEGRAM_TOKEN
from handlers import router
from scheduler import main as scheduler_main

from database import init_db


async def main():
    # Ensure the database is initialized
    init_db()

    bot = Bot(token=TELEGRAM_TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    dp.include_router(router)

    # Start the scheduler
    asyncio.create_task(scheduler_main())

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
