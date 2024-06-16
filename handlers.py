from aiogram import Router, types
from aiogram.filters import CommandStart, Command
from models import get_user_by_chat_id, create_user, log_message, schedule_message
from datetime import datetime, timedelta
from llm_provider import generate_responce

router = Router()

BOT_NAME = "SleepWellBot"
FORM_LINK = "https://form.typeform.com/to/Wv8KDBuG"

@router.message(CommandStart())
async def start(message: types.Message):
    user = get_user_by_chat_id(message.chat.id)
    if user:
        await message.answer("Welcome back!")
    else:
        create_user(message.from_user.username, message.chat.id)
        await message.answer(f"Welcome to the {BOT_NAME}! 🌙 It seems you're not registered yet. Complete our circadian \
    assessment to get recommendations that align with your internal clocks! Here is the link: {FORM_LINK}")
        await message.answer("Welcome! You are now registered.")

@router.message()
async def echo(message: types.Message):
    user = get_user_by_chat_id(message.chat.id)
    if user:
        log_message(user.id, message.text)
        responce = generate_responce(request=message.text, user_name=message.from_user.username, history='')

        await message.answer(f"{responce}")
    else:
        await message.answer("You need to /start first.")



@router.message(Command(commands=["schedule"]))
async def schedule(message: types.Message):
    user = get_user_by_chat_id(message.chat.id)
    if user:
        parts = message.text.split(maxsplit=2)
        if len(parts) < 3:
            await message.answer("Usage: /schedule <minutes_from_now> <message>")
            return
        try:
            minutes_from_now = int(parts[1])
        except ValueError:
            await message.answer("Invalid time format.")
            return
        schedule_time = datetime.now() + timedelta(minutes=minutes_from_now)
        schedule_message(user.id, parts[2], schedule_time)
        await message.answer(f"Message scheduled for {schedule_time}.")
    else:
        await message.answer("You need to /start first.")
