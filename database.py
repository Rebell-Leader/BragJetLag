from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

DATABASE_URL = 'sqlite:///database.db'

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    chat_id = Column(Integer, unique=True, index=True)

class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    message = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

class ScheduledMessage(Base):
    __tablename__ = 'scheduled_messages'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    message = Column(String)
    send_at = Column(DateTime)
    sent = Column(Boolean, default=False)

Base.metadata.create_all(bind=engine)

# Ensure the database tables are created
def init_db():
    Base.metadata.create_all(bind=engine)

# Call the init_db function to create the tables if they don't exist
init_db()
