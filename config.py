import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///database.db')
SQLALCHEMY_TRACK_MODIFICATIONS=os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', False)
TELEGRAM_TOKEN=os.getenv('TELEGRAM_TOKEN', 'TOKEN')
FLIGHT_API_KEY=os.getenv('FLIGHT_API_KEY', '')
OPENAI_API_KEY=os.getenv('OPENAI_API_KEY', '')
