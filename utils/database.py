import sqlalchemy as db
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pandas as pd
from datetime import datetime

Base = declarative_base()

class Employee(Base):
    __tablename__ = 'employees'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)
    role = Column(String)       # 'employee' or 'hr'
    name = Column(String)
    team = Column(String)

class MoodRecord(Base):
    __tablename__ = 'mood_records'
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)
    text_mood = Column(String)
    facial_mood = Column(String)
    speech_mood = Column(String)
    final_mood = Column(String)
    stress_level = Column(Float)
    productivity_score = Column(Float)
    recommended_task = Column(String)
    task_accepted = Column(String)   # 'yes' / 'no' / 'pending'

class Alert(Base):
    __tablename__ = 'alerts'
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)
    alert_type = Column(String)    # 'high_stress', 'burnout_risk'
    severity = Column(String)
    message = Column(String)
    acknowledged = Column(Integer, default=0)

engine = create_engine('sqlite:///data/mood_history.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def get_session():
    return Session()

def add_mood_record(emp_id, text_mood, facial_mood, speech_mood, final_mood,
                    stress, productivity, rec_task, task_accepted='pending'):
    session = get_session()
    record = MoodRecord(employee_id=emp_id, text_mood=text_mood,
                        facial_mood=facial_mood, speech_mood=speech_mood,
                        final_mood=final_mood, stress_level=stress,
                        productivity_score=productivity,
                        recommended_task=rec_task, task_accepted=task_accepted)
    session.add(record)
    session.commit()
    session.close()

def get_employee_moods(emp_id, days=30):
    session = get_session()
    from datetime import timedelta
    since = datetime.utcnow() - timedelta(days=days)
    records = session.query(MoodRecord).filter(
        MoodRecord.employee_id == emp_id,
        MoodRecord.timestamp >= since
    ).order_by(MoodRecord.timestamp.desc()).all()
    session.close()
    return records

def get_all_moods(days=30):
    session = get_session()
    from datetime import timedelta
    since = datetime.utcnow() - timedelta(days=days)
    records = session.query(MoodRecord).filter(
        MoodRecord.timestamp >= since
    ).all()
    session.close()
    return records

def add_alert(emp_id, alert_type, severity, message):
    session = get_session()
    alert = Alert(employee_id=emp_id, alert_type=alert_type,
                  severity=severity, message=message)
    session.add(alert)
    session.commit()
    session.close()

def get_alerts(acknowledged=False):
    session = get_session()
    if acknowledged:
        alerts = session.query(Alert).filter(Alert.acknowledged == 0).all()
    else:
        alerts = session.query(Alert).all()
    session.close()
    return alerts