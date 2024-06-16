from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import SystemMessage
from langgraph.checkpoint import MemorySaver

from config import OPENAI_API_KEY


@tool
def flight_info_tool(flight_id: str) -> str:
    '''GetFlightInfo - Use this tool to search for the flight information by flight ID'''
    return 'None'


@tool
def schedule_message_tool(user_id: str, msg: str, send_datetime: str) -> str:
    '''ScheduleAlert - Use this tool to send the message to a user in a particular time'''
    #schedule the message and also add to db table
    print(f'Planning to send the MSG {msg} to user {user_id} on {send_datetime}')
    return 'All set'


def generate_responce(user_request):
    tools = [flight_info_tool, schedule_message_tool]
    SYSTEM_PROMPT = '''You are an expert in designing personalized, science-backed sleep and circadian protocols.
    Your goal is to create a detailed, tailored plan that addresses an individual's chronotype and preferences,
    with the aim of enhancing their sleep quality and daytime alertness for dealing with jet lag. Your recommendations
    should be actionable and time-specific. You need to develop the recommendations for User to follow, and plan to send them in an appropriate time (like a reminder to go to sleep in time, or take melatonin 30 minutes before sleeping), using the provided Tools.
    You must use tool "GetFlightInfo" (flight_info_tool tool name), to search for the flight by the flight number provided by User. If nothing is found, just ask the User about the departure and arrival time and locations (remember about the different timezones!).
    You also have to use the tool called ScheduleAlert (schedule_message_tool tool name) to schedule the messages for the user, for the particular time.
    For your convenience, you will see the list of entities from the dialog history, and some info about the user, as well as the recommendation example for another user.
    '''


    USER_PROMPT = """Based on the provided circadian assessment (user's personal assessment), generate recommendations \
    that are targeting melatonin, caffeine, physical activity, light exposure, sleep onset and offset timing.
    """
    suffix = """Begin the dialog with the user"
    Entities from the dialog: {entities}
    Question: {user_request}
    User info: {user_info}
    Recommendation example: {recommendation_example}
    {agent_scratchpad}"""

    recommendation_example = '''Hi {Name}, for your flight from {origin} to {destination} on {date}, \
        here is my recommendations for optimizing your sleep and alertness for today:
    🌞 Take 0.5mg melatonin at 10:30pm to help advance your sleep onset
    ☕ Avoid caffeine after 3pm
    🌇 Get outdoor light exposure in the morning to help anchor your circadian clock
    🚶‍♂️ Do some light exercise like walking between 5-7pm

    This gradual adjustment shifts the sleep-wake cycle ahead before your trip.'''

    user_info = '''What is your name?	What is your number? This way I can communicate tips to you.	What is your age?	Which problems do you have related to sleep, if any?	What have you used to improve your sleep?	What is your typical bed time and wake-up time *on weekdays*?	What is your typical bed time and wake-up time *on weekends*?	During the past month, how long does it typically take you to fall asleep after going to bed (in min)?	How many hours of sleep do you typically get per night (in hours)?	Do you experience difficulty waking up in the morning, even after getting enough sleep?	Do you consider yourself a “morning person” or a “night owl”?	Do you need an alarm to wake up on most days? 	How long after waking up does it typically take you to feel fully alert and focused? 	When do you feel most alert and productive?	When do you prefer engaging in mentally demanding activities (like analysis, writing, coding)?
    Kevin	+14157875337	35	Excessive daytime sleepiness, Difficulty waking up or getting out of bed	Supplements (e.g. melatonin), Changing surroundings (e.g. sleep mask, blackout curtains), Mindfulness and meditation, Exercise	1 am - 8 am	2 am - 10 am	15	8	ЛОЖЬ	Night Owl	ИСТИНА	30 min to 1h	Evening	Morning, Evening'''


    #non-authorized
    welcome_message = '''Welcome to the {bot name}! 🌙 It seems you're not registered yet. Complete our circadian \
        assessment to get recommendations that align with your internal clocks! Here is the link: https://form.typeform.com/to/Wv8KDBuG'''


    memory = MemorySaver()

    formed_system_prompt = f'{SYSTEM_PROMPT} \n {USER_PROMPT} \n {suffix} \n Recommendation example: {recommendation_example} \n User info: {user_info}'

    model = ChatOpenAI(temperature=1, openai_api_key=OPENAI_API_KEY, model="gpt-4o")

    app = create_react_agent(model, tools, messages_modifier=formed_system_prompt, checkpointer=memory)
    config = {"configurable": {"thread_id": "main-thread"}}

    messages = app.invoke({"messages": [("human", user_request)]}, config)
    request_responce = {
        "input": user_request,
        "output": messages["messages"][-1].content,
    }

    return messages["messages"][-1].content

