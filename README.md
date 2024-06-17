# BragJetLag
BragJetLag is a Telegram LLM-powered chatbot that generates personalized recommendations for a user having a flight.

This chatbot can search for the exact flight by date and time using Skyscanner API (#TODO migrate to stable API) and send user notifications at a particular time with exact recommendations. The recommendations are based on the user's assessment data and flight information.

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
4. Run the bot with
