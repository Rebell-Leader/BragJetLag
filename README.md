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
SYSTEM_PROMPT = """As an expert in sleep and circadian protocols, your task is to create personalized plans for individuals dealing with jet lag. These plans should consider the person’s chronotype, preferences, and actionable steps to improve sleep quality and daytime alertness."""
USER_PROMPT = """Using the user’s circadian assessment, provide recommendations related to melatonin, caffeine, physical activity, light exposure, and optimal sleep onset and offset timing.
"""
## Message suggestions:
Recommendations
"Hello {Name}, for your upcoming flight from {origin} to {destination} on {date}, consider the following recommendations to optimize your sleep and alertness:
🌞 Take 0.5mg of melatonin at 10:30pm to advance your sleep onset.
☕ Avoid caffeine consumption after 3pm.
🌇 Get outdoor light exposure in the morning to anchor your circadian clock.
🚶‍♂️ Engage in light exercise, such as walking, between 5pm and 7pm.
These adjustments will help shift your sleep-wake cycle before your trip."

## Welcome message:
Welcome to {bot name}! 🌙 If you haven’t registered yet, complete our circadian assessment to receive personalized recommendations aligned with your internal clocks.
## Dialog example:
 - User: In July I have a flight from Paris to Mexico - please give me some advice for healthy sleeping habits
 - Bot: To assist you better, could you please provide me with your flight number? If you don't have it handy, you can also let me know your exact departure and arrival times for your flight from Paris to Mexico. This information will help me to accurately create a sleep and alertness optimization plan for you.
 - User: The flight is on 23.07.2024. The flight number is TE-ST14, from 09:15 to 19:40. Give me some recommendations to prepare for the flight and sleep well
 - Bot: Could you please confirm the exact departure and arrival times and locations for your flight on July 23rd, 2024 from Paris to Mexico? It appears I couldn't find any information based on the flight number.
 - User: That's correct, it is the charter flight
 - Bot: Here are your personalized recommendations and scheduled reminders for your upcoming trip from Paris to Mexico:

### Before the Flight
Three Days Before Departure (20th July):
🌞 Morning Light Exposure: Get natural light exposure within 30 minutes of waking up for at least 30 minutes. This helps anchor your circadian rhythm.
🌙 Melatonin: Take 0.5mg of melatonin at 11:15 PM to help shift your sleep cycle earlier.
☕️ Avoid Caffeine: Refrain from consuming caffeine after 3:00 PM.
Two Days Before Departure (21st July):
🌞 Morning Light Exposure: Continue your morning light exposure routine.
🌙 Melatonin: Take 0.5mg of melatonin at 11:00 PM.
☕️ Avoid Caffeine: Maintain caffeine avoidance after 3:00 PM.
🚶‍♂️ Evening Exercise: Engage in light exercise, such as walking, between 5:00 PM and 7:00 PM. This promotes alertness during the day and better sleep at night.
Day Before Departure (22nd July):
🌞 Morning Light Exposure: Keep up with your morning light exposure.
🌙 Melatonin: Take 0.5mg of melatonin at 10:45 PM.
☕️ Avoid Caffeine: Continue avoiding caffeine after 3:00 PM.
🚶‍♂️ Evening Exercise: Again, engage in light exercise between 5:00 PM and 7:00 PM.
Day of the Flight (23rd July):
Sleep Timing: Try to wake up by 6:15 AM to begin adjusting to the Mexico time zone.
During the Flight:
🌙 Melatonin: Take 0.5mg of melatonin 30 minutes before you plan to sleep on the plane. This helps synchronize your internal clock.
💦 Stay Hydrated: Drink plenty of water during the flight.
🍎 Light Meals: Opt for light, easily digestible meals.
💡 Light Management: Use a sleep mask to block light during sleep periods on the plane. Also, try to get natural light exposure during Mexico’s daylight hours.
After Arrival (23rd July):
🌞 Light Exposure: Upon arrival, seek natural sunlight exposure to reset your internal clock.
Sleep Schedule: Stay awake until at least 10:00 PM Mexico time to adjust your sleep schedule.
Meal Timing: Align your meals with the local time.
I’ve also set up reminders for each action to help you stay on track. Safe travels, and feel free to ask if you need further adjustments or have any questions! 😊
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
5. Add Admin ID to .env and admin panel to manage users (and their profile info), notifications, flights and so on - editing and removing DB entries.
