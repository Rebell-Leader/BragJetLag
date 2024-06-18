from database import SessionLocal, User, Message, ScheduledMessage
from datetime import datetime

def get_user_by_chat_id(chat_id: int):
    session = SessionLocal()
    return session.query(User).filter(User.chat_id == chat_id).first()

#Here are the functions to work with persistent objects from database
def create_user(username: str, chat_id: int):
    session = SessionLocal()
    user = User(username=username, chat_id=chat_id)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def log_message(user_id: int, message: str):
    session = SessionLocal()
    msg = Message(user_id=user_id, message=message)
    session.add(msg)
    session.commit()
    return msg


def schedule_message(user_id: int, message: str, send_at: datetime):
    session = SessionLocal()
    scheduled_msg = ScheduledMessage(user_id=user_id, message=message, send_at=send_at)
    session.add(scheduled_msg)
    session.commit()
    return scheduled_msg


def get_pending_messages():
    session = SessionLocal()
    return session.query(ScheduledMessage).filter(ScheduledMessage.sent == False, ScheduledMessage.send_at <= datetime.utcnow()).all()


def mark_message_as_sent(message_id: int):
    session = SessionLocal()
    msg = session.query(ScheduledMessage).filter(ScheduledMessage.id == message_id).first()
    msg.sent = True
    session.commit()
    return msg
