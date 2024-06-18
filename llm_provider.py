from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import SystemMessage
from langgraph.checkpoint import MemorySaver
import random
import datetime
from datetime import timedelta
from models import schedule_message

from config import OPENAI_API_KEY

#define the tools
@tool
def flight_info_tool(flight_id: str) -> str:
    '''GetFlightInfo - Use this tool to search for the flight information by flight ID'''
    return f'No info about flight {flight_id}. Please refer to date and time provided by user.'


@tool
def schedule_message_tool(user_id: str, msg: str, send_datetime_delta: str) -> str:
    '''ScheduleAlert - Use this tool to send the message to a user in a particular time (as a timedelta in minutes from now).'''
    #schedule the message and also add to db table

    schedule_time = datetime.datetime.now() + timedelta(minutes=int(send_datetime_delta))

    print(f'Planning to send the MSG {msg} to user {user_id} on {schedule_time}')

    schedule_message(user_id, msg, schedule_time)

    return 'All set'

#add mock function to load user assessment data
def get_user_assessment_data(user_name) -> str:
    field_data = 'What is your name?	What is your number? This way I can communicate tips to you.	What is your age?	Which problems do you have related to sleep, if any?	What have you used to improve your sleep?	What is your typical bed time and wake-up time *on weekdays*?	What is your typical bed time and wake-up time *on weekends*?	During the past month, how long does it typically take you to fall asleep after going to bed (in min)?	How many hours of sleep do you typically get per night (in hours)?	Do you experience difficulty waking up in the morning, even after getting enough sleep?	Do you consider yourself a “morning person” or a “night owl”?	Do you need an alarm to wake up on most days? 	How long after waking up does it typically take you to feel fully alert and focused? 	When do you feel most alert and productive?	When do you prefer engaging in mentally demanding activities (like analysis, writing, coding)?'
    user_data_list = ['Kevin	+14157875337	35	Excessive daytime sleepiness, Difficulty waking up or getting out of bed	Supplements (e.g. melatonin), Changing surroundings (e.g. sleep mask, blackout curtains), Mindfulness and meditation, Exercise	1 am - 8 am	2 am - 10 am	15	8	ЛОЖЬ	Night Owl	ИСТИНА	30 min to 1h	Evening	Morning, Evening', 'Shelley	17657484758	72	Difficulty falling asleep, Difficulty waking up or getting out of bed	Supplements (e.g. melatonin), Exercise	2am-11am	3am-12pm	20	6	TRUE	Night Owl	TRUE	30 min to 1h	Evening	Evening', 'Ash	17658082359	25	Difficulty waking up or getting out of bed, Excessive daytime sleepiness, Difficulty staying asleep	Prescription medication (e.g. trazodone, Ambien), Exercise, None	10pm - 7am	2am - 12pm	35	7	TRUE	I don\'t know	FALSE	Less than 30 min	Morning	Afternoon', 'Niko	9,96E+11	29	Physical symptoms (e.g. headaches, pain), Difficulty falling asleep	Changing surroundings (e.g. sleep mask, blackout curtains), Supplements (e.g. melatonin)	01am-10pm	1am-10am	30	8	FALSE	afternoon person	TRUE	30 min to 1h	Afternoon	Evening', 'Megan	14157875448	65	Emotional symptoms (e.g. irritability, depression), Difficulty staying asleep, Difficulty falling asleep	Prescription medication (e.g. trazodone, Ambien), Changing surroundings (e.g. sleep mask, blackout curtains)	10 pm - 6 am	10 pm - 6 am	40	8	FALSE	Morning Person	FALSE	I don\'t know	Morning	Morning', 'AAA	79013871127	25	Difficulty falling asleep, Difficulty staying asleep	Supplements (e.g. melatonin)	11 pm - 8 am	11 pm - 8 am	20	8	FALSE	Morning Person	TRUE	Less than 30 min	Morning	Morning', 'g	12015550123	23	Difficulty falling asleep	Supplements (e.g. melatonin)	11	11	35	5	FALSE	Morning Person	FALSE	I don\'t know	I don\'t know	I don\'t know']
    random_assessment = random.choice(user_data_list)
    return f'Assessment for {user_name}. {field_data}: {random_assessment}'

#add main function to generate response with openAI LLM agent
def generate_response(user_request, user_name, user_id):
    tools = [flight_info_tool, schedule_message_tool]
    SYSTEM_PROMPT = '''You are an expert in designing personalized, science-backed sleep and circadian protocols.
    Your goal is to create a detailed, tailored plan that addresses an individual's chronotype and preferences,
    with the aim of enhancing their sleep quality and daytime alertness for dealing with jet lag. Your recommendations
    should be actionable and time-specific. You need to develop the recommendations for User to follow, and plan to send them in an appropriate time (like a reminder to go to sleep in time, or take melatonin 30 minutes before sleeping), using the provided Tools.
    You must use tool "GetFlightInfo" (flight_info_tool tool name), to search for the flight by the flight number provided by User. If nothing is found, just ask the User about the departure and arrival time and locations (remember about the different timezones!).
    You also have to use the tool called ScheduleAlert (schedule_message_tool tool name) to schedule the messages for the user, for the particular time (provide message text and delta in minutes from now).
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

    user_info = get_user_assessment_data(user_name)
    #add current date ana time to set the scheduler properly
    date_time = datetime.datetime.now()

    memory = MemorySaver()

    formed_system_prompt = f'{SYSTEM_PROMPT} \n {USER_PROMPT} \n {suffix} \n Exact date and time is {date_time}\n User ID is {user_id}. \n Recommendation example: {recommendation_example} \n User info: {user_info}'

    model = ChatOpenAI(temperature=1, openai_api_key=OPENAI_API_KEY, model="gpt-4o")

    app = create_react_agent(model, tools, messages_modifier=formed_system_prompt, checkpointer=memory)
    config = {"configurable": {"thread_id": "main-thread"}}

    messages = app.invoke({"messages": [("human", user_request)]}, config)

    return messages["messages"][-1].content

