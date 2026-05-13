import streamlit as st
import pandas as pd
import plotly.express as px
from utils.database import get_all_moods, get_alerts, get_session, Employee, Alert
from utils.privacy import anonymize_employee_id

st.title("👥 HR Team Wellness Dashboard")

# Alerts section
st.subheader("🚨 Active Alerts")
alerts = get_alerts(acknowledged=False)
if alerts:
    for a in alerts:
        emp_name = get_session().query(Employee).filter_by(id=a.employee_id).first().name
        st.warning(f"{a.severity.upper()}: {emp_name} - {a.message} ({a.timestamp.strftime('%Y-%m-%d %H:%M')})")
        if st.button(f"Acknowledge {a.id}", key=f"ack_{a.id}"):
            sess = get_session()
            alert = sess.query(Alert).get(a.id)
            alert.acknowledged = 1
            sess.commit()
            st.experimental_rerun()
else:
    st.success("No active alerts.")

# Team mood distribution
st.subheader("📊 Team Mood Distribution (Last 7 Days)")
records = get_all_moods(days=7)
if records:
    df = pd.DataFrame([{
        'employee': anonymize_employee_id(r.employee_id),
        'mood': r.final_mood,
        'stress': r.stress_level,
        'productivity': r.productivity_score,
        'timestamp': r.timestamp
    } for r in records])
    fig1 = px.pie(df, names='mood', title='Mood Distribution')
    st.plotly_chart(fig1, use_container_width=True)

    fig2 = px.bar(df.groupby('employee').agg({'stress':'mean','productivity':'mean'}).reset_index(),
                  x='employee', y='stress', color='productivity',
                  title='Average Stress & Productivity per Employee')
    st.plotly_chart(fig2, use_container_width=True)

    fig3 = px.line(df.sort_values('timestamp'), x='timestamp', y='stress', color='employee',
                   title='Stress Trends')
    st.plotly_chart(fig3, use_container_width=True)