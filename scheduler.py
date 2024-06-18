import asyncio
from aiogram import Bot
from config import TELEGRAM_TOKEN
from models import get_pending_messages, mark_message_as_sent

bot = Bot(token=TELEGRAM_TOKEN)
#define the scheduler
async def send_scheduled_messages():
    while True:
        pending_messages = get_pending_messages()
        for msg in pending_messages:
            try:
                await bot.send_message(msg.user_id, msg.message)
                mark_message_as_sent(msg.id)
            except Exception as e:
                print(f"Failed to send message: {e}")
        await asyncio.sleep(60)

async def main():
    await send_scheduled_messages()
