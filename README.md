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

## Dialog example:
User: In July I have a flight from Paris to Mexico - please give me some advice for healthy sleeping habits
Bot: To assist you better, could you please provide me with your flight number? If you don't have it handy, you can also let me know your exact departure and arrival times for your flight from Paris to Mexico. This information will help me to accurately create a sleep and alertness optimization plan for you.
User: The flight is on 23.07.2024. The flight number is TE-ST14, from 09:15 to 19:40. Give me some recommendations to prepare for the flight and sleep well
Bot: Could you please confirm the exact departure and arrival times and locations for your flight on July 23rd, 2024 from Paris to Mexico? It appears I couldn't find any information based on the flight number.
User: That's correct, it is the charter flight
Bot: Here are your personalized recommendations and scheduled reminders for your upcoming trip from Paris to Mexico:

### Before the Flight

#### Three Days Before Departure (20th July):
- 🌞 **Morning Light Exposure**: Get light exposure within 30 minutes of waking up for at least 30 minutes.
- 🌙 **Melatonin**: Take 0.5mg melatonin at 11:15 PM to help shift your sleep cycle earlier.
- ☕️ **Avoid Caffeine**: Avoid caffeine after 3:00 PM.

#### Two Days Before Departure (21st July):
- 🌞 **Morning Light Exposure**: Continue morning light exposure.
- 🌙 **Melatonin**: Take 0.5mg melatonin at 11:00 PM.
- ☕️ **Avoid Caffeine**: Avoid caffeine after 3:00 PM.
- 🚶‍♂️ **Evening Exercise**: Engage in light exercise like walking between 5:00 PM - 7:00 PM.

#### Day Before Departure (22nd July):
- 🌞 **Morning Light Exposure**: Keep up with the morning light exposure.
- 🌙 **Melatonin**: Take 0.5mg melatonin at 10:45 PM.
- ☕️ **Avoid Caffeine**: Avoid caffeine after 3:00 PM.
- 🚶‍♂️ **Evening Exercise**: Engage in light exercise between 5:00 PM - 7:00 PM.

### Day of the Flight (23rd July):
- **Sleep**: Try to wake up by 6:15 AM to begin shifting to the Mexico time zone.
- **During the Flight**:
  - 🌙 **Melatonin**: Take 0.5mg melatonin 30 minutes before you plan to sleep on the plane to help you adjust.
  - 💦 **Hydration**: Stay hydrated by drinking plenty of water.
  - 🍎 **Light Meals**: Eat light and easily digestible meals.
  - 💡 **Light Management**: Use a sleep mask to block light during sleep periods on the plane and try to get light exposure during Mexico’s daylight hours.

### After Arrival (23rd July):
- 🌞 **Light Exposure**: Upon arrival, get natural sunlight exposure to help reset your internal clock.
- **Sleeping Schedule**: Try to stay awake until at least 10:00 PM Mexico time to adjust your sleep schedule.
- **Meal Timing**: Eat in alignment with the local time.

I have set up reminders for you to make sure you follow through with the actions:

1. 🌞 Start getting light exposure on 20th July.
2. 🌙 Take melatonin at 11:15 PM on 20th July.
3. ☕️ Avoid caffeine after 3:00 PM on 20th July.
4. 🌞 Continue morning light exposure on 21st July.
5. 🌙 Take melatonin at 11:00 PM on 21st July.
6. 🚶‍♂️ Evening exercise on 21st July.
7. 🌞 Keep up with morning light exposure on 22nd July.
8. 🌙 Take melatonin at 10:45 PM on 22nd July.
9. 🚶‍♂️ Evening exercise on 22nd July.
10. Wake up by 6:15 AM on 23rd July.
11. **During the flight**:
    - 🌙 Take melatonin 30 minutes before you plan to sleep.
    - 💦 Stay hydrated.
    - 🍎 Light meals.
    - 💡 Use a sleep mask.

Safe travels and enjoy your trip! If you need any additional adjustments or have further questions, feel free to ask.

## Running the Application in Docker

1. Build the Docker image: `docker build -t flight-recommendations-chatbot .`
2. Run the Docker container: `docker run -d --name flight-recommendations-chatbot --env-file .env flight-recommendations-chatbot`

## Running the Application locally

1. Create a virtual environment: `python -m venv venv` and activate it `source venv/bin/activate`
2. Install requirements: `pip install -r requirements.txt`
3. Fill out the .env file, using the .env.example template: prepare the Telegram and OpenAI API keys.
4. Run the bot with `python bot.py`


## Limitations and space for improvement
1. User registration is done via Telegram, without any phone number or email - add this info to the user profile after authorization (with confirmation).
2. The interaction with the flight API is currently mocked up - need to use the real API provider (or search + crawler, because we only need the flight date and time + time zones, nothing complex).
3. Currently there is no user profile button in the Telegram bot - add the list of flights, list of recommendations for each flight, and notifications.
4. Move the sleep assessment from the separate form to the TG bot itself, to the route after the user registration. Add assessment results to the user profile with the button to update the assessment results.
