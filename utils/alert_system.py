from utils.database import get_session, Alert, MoodRecord
from datetime import datetime, timedelta
import pandas as pd

STRESS_THRESHOLD = 0.7
BURNOUT_CONSECUTIVE_DAYS = 5

def check_stress_alerts(emp_id):
    """Check recent moods and trigger alerts if needed."""
    session = get_session()
    cutoff = datetime.utcnow() - timedelta(days=7)
    records = session.query(MoodRecord).filter(
        MoodRecord.employee_id == emp_id,
        MoodRecord.timestamp >= cutoff
    ).order_by(MoodRecord.timestamp.desc()).all()
    session.close()

    if not records:
        return

    df = pd.DataFrame([{
        'timestamp': r.timestamp,
        'stress_level': r.stress_level,
        'final_mood': r.final_mood
    } for r in records])

    # High stress today
    if not df.empty and df.iloc[0]['stress_level'] >= STRESS_THRESHOLD:
        add_alert_if_new(emp_id, 'high_stress', 'High',
                         f"Stress level {df.iloc[0]['stress_level']:.2f} exceeded threshold.")

    # Burnout risk: stress > 0.6 for 5 consecutive days
    if len(df) >= BURNOUT_CONSECUTIVE_DAYS:
        recent = df.head(BURNOUT_CONSECUTIVE_DAYS)
        if all(recent['stress_level'] > 0.6):
            add_alert_if_new(emp_id, 'burnout_risk', 'Critical',
                             f"Burnout risk detected: stress > 0.6 for {BURNOUT_CONSECUTIVE_DAYS} days.")

def add_alert_if_new(emp_id, alert_type, severity, message):
    session = get_session()
    exists = session.query(Alert).filter_by(
        employee_id=emp_id, alert_type=alert_type, message=message,
        acknowledged=0
    ).first()
    if not exists:
        alert = Alert(employee_id=emp_id, alert_type=alert_type,
                      severity=severity, message=message)
        session.add(alert)
        session.commit()
    session.close()