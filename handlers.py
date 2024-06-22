from aiogram import Router, Bot, F, types
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
import functools

from models import get_user_by_chat_id, create_user, log_message, schedule_message
from datetime import datetime, timedelta
from llm_provider import generate_response
from config import DEBUG_MODE, MAX_TELEGRAM_MESSAGE_LEN



router = Router()

#set project-level variables here
BOT_NAME = "SleepWellBot"
FORM_LINK = "https://form.typeform.com/to/Wv8KDBuG"


# In-memory chat history storage (dictionary)
chat_history = {}

async def store_chat_history(user_id, message_text):
  """Stores message for a user in the in-memory dictionary"""
  if user_id not in chat_history:
    chat_history[user_id] = []
  chat_history[user_id].append(message_text)

async def retrieve_chat_history(user_id, max_messages=5):
  """Retrieves the last N messages from chat history for a user"""
  if user_id not in chat_history:
    return []
  return chat_history[user_id][-max_messages:]

async def format_chat_history_as_prompt(chat_history):
  """Formats chat history as a single string prompt"""
  prompt = "Previous conversation:\n"
  for message in chat_history:
    prompt += f"- {message}\n"
  return prompt.strip()



def process_error(error_message: str) -> str:
    """Translates the message to human and adds Markdown style."""

    # Handle OpenAI location restriction.
    if "unable_to_access" in error_message:
        error_message = (
            "Most likely your requests for OpenAI are blocked due to your "
            "region. Try using a VPN or deploying the bot on a server in a "
            "different region."
        )

    error_message = error_message[:MAX_TELEGRAM_MESSAGE_LEN - 13]
    return f"```Error: {error_message}```"


def debug_handler_reply(handler):
    """Replies on message with raised error message."""

    @functools.wraps(handler)
    async def wrapper(message: Message, *args, **kwargs):
        if not isinstance(message, Message):
            return await handler(message, *args, **kwargs)

        try:
            return await handler(message, *args, **kwargs)
        except Exception as e:
            if DEBUG_MODE:
                error_message = process_error(str(e))
                await message.reply(text=error_message, parse_mode="Markdown")
            raise
    return wrapper


#Start dialog route
@router.message(CommandStart())
async def start(message: types.Message):
    user = get_user_by_chat_id(message.chat.id)
    if user:
        #authorized user with no assessment passed
        await message.answer("Welcome back! Are you planning a flight?")
        await message.answer(f"You are already registered. Make sure to complete our circadian assessment to get recommendations that align with your internal clocks! Here is the link: {FORM_LINK}")
    else:
        #TODO authorize user and save the username properly, move assessment from external form to a separate TG route, save assessment results to DB
        #non-authorized user, register and send assessment link
        create_user(message.from_user.username, message.chat.id)
        await message.answer(f"Welcome to the {BOT_NAME}! 🌙 It seems you're not registered yet. Complete our circadian assessment to get recommendations that align with your internal clocks! Here is the link: {FORM_LINK}")
        await message.answer("Welcome! You are now registered.")


#Normal dialog with Agent
@router.message()
async def chat_with_agent(message: types.Message):
    user = get_user_by_chat_id(message.chat.id)
    if user:
        log_message(user.id, message.text)

        user_id = message.from_user.id
        message_text = message.text

        # Store chat history
        await store_chat_history(user_id, message_text)

        # Retrieve recent chat history
        recent_history = await retrieve_chat_history(user_id)

        # Format prompt
        prompt = await format_chat_history_as_prompt(recent_history)
        response = generate_response(user_request=prompt, user_name=message.from_user.username, user_id=message.from_user.id)
        await message.answer(response)
    else:
        await message.answer("You need to /start first.")
