import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import random
from datetime import datetime, timedelta
from utils.database import Base, Employee, MoodRecord, engine
from sqlalchemy.orm import sessionmaker

# This script populates the database with dummy employees and mood history.
# Run from project root with: python data/synthetic_data.py

# Ensure tables are created
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Add employees
employees = [
    Employee(username='emp1', password='password123', role='employee', name='Alice Chen', team='Engineering'),
    Employee(username='emp2', password='password123', role='employee', name='Bob Smith', team='Design'),
    Employee(username='emp3', password='password123', role='employee', name='Carol Davis', team='Marketing'),
    Employee(username='hr1', password='hrpass123', role='hr', name='HR Manager', team='HR'),
]
session.add_all(employees)
session.commit()

# Generate mood records for the past 30 days
moods = ['happy', 'neutral', 'sad', 'stressed', 'tired', 'focused']
for emp in employees[:3]:
    for day in range(30):
        timestamp = datetime.now() - timedelta(days=30 - day)
        mood = random.choice(moods)
        stress = round(random.uniform(0.1, 0.9), 2)
        prod = round(random.uniform(0.3, 1.0), 2)
        rec_task = random.choice(['Creative', 'Analytical', 'Light', 'Break'])
        record = MoodRecord(
            employee_id=emp.id,
            timestamp=timestamp,
            text_mood=mood,
            facial_mood=mood,
            speech_mood=mood,
            final_mood=mood,
            stress_level=stress,
            productivity_score=prod,
            recommended_task=rec_task,
            task_accepted='yes'
        )
        session.add(record)

session.commit()
session.close()
print("Synthetic data generated successfully.")