# BragJetLag
BragJetLag is a Telegram LLM-powered chatbot that generates personalized recommendations for a user having a flight.

This chatbot can search for the exact flight by date and time using Skyscanner API (#TODO migrate to stable API) and send user notifications at a particular time with exact recommendations. The recommendations are based on the user's assessment data and flight information.

## Project Structure
* __init__.py Initializes the app module.
* bot.py Main entry point for the bot. Sets up the bot, dispatcher, and starts polling. Also initializes the scheduler.
* config.py Contains configuration variables such as the Telegram API token and the database URL. Loads environment variables using python-dotenv.
* database.py Sets up the SQLite database using SQLAlchemy. Defines the User, Message, and ScheduledMessage models. Contains the init_db function to create tables if they don't exist.
* handlers.py Contains the command and message handlers for the bot. Handles user registration, logging messages, and scheduling messages.
* scheduler.py Manages scheduled messages using APScheduler. Defines functions for scheduling messages, loading scheduled messages from the database, and sending messages at the specified times.
* models.py Contains functions for interacting with the database, such as creating users, logging messages, and scheduling messages.
* requirements.txt Lists the Python dependencies required for the project, including aiogram, SQLAlchemy, python-dotenv, and APScheduler.
* Dockerfile Docker configuration file for containerizing the application. Sets up the Python environment, installs dependencies, and runs the bot.
* .env Environment variables file. Should include the Telegram bot token and any other sensitive configuration data.



## Prompt examples
SYSTEM_PROMPT = "You are an expert in designing personalized, science-backed sleep and circadian protocols. Your goal is to create a detailed, tailored plan that addresses an individual's chronotype and preferences, with the aim of enhancing their sleep quality and daytime alertness for dealing with jet lag. Your recommendations should be actionable and time-specific."

USER_PROMPT = """Based on the provided circadian assessment (user's personal assessment), generate recommendations that are targeting melatonin, caffeine, physical activity, light exposure, sleep onset and offset timing.
"""
## Message suggestions:
Recommendations
“Hi {Name}, for your flight from {origin} to {destination} on {date}, here is my recommendations for optimizing your sleep and alertness for today:
🌞 Take 0.5mg melatonin at 10:30pm to help advance your sleep onset
☕ Avoid caffeine after 3pm
🌇 Get outdoor light exposure in the morning to help anchor your circadian clock
🚶‍♂️ Do some light exercise like walking between 5-7pm
This gradual adjustment shifts the sleep-wake cycle ahead before your trip.”

## Welcome message:
Welcome to the {bot name}! 🌙 It seems you're not registered yet. Complete our circadian assessment to get recommendations that align with your internal clocks!


## Running the Application in Docker

1. Build the Docker image: `docker build -t flight-recommendations-chatbot .`
2. Run the Docker container: `docker run -d --name flight-recommendations-chatbot --env-file .env flight-recommendations-chatbot`

## Running the Application locally

1. Create a virtual environment: `python -m venv venv` and activate it `source venv/bin/activate`
2. Install requirements: `pip install -r requirements.txt`
3. Fill out the .env file, using the .env.example template: prepare the Telegram and OpenAI API keys.
4. Run the bot with `python bot.py`
