import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils.database import get_employee_moods, get_session, Employee

st.title("📈 Historical Analytics")

emp_id = st.session_state.emp_id
days = st.slider("Select days to analyze", 7, 90, 30)
records = get_employee_moods(emp_id, days=days)
if records:
    df = pd.DataFrame([{
        'date': r.timestamp.date(),
        'mood': r.final_mood,
        'stress': r.stress_level,
        'productivity': r.productivity_score
    } for r in records])
    daily = df.groupby('date').agg({'stress':'mean','productivity':'mean'}).reset_index()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=daily['date'], y=daily['stress'], name='Stress', line=dict(color='red')))
    fig.add_trace(go.Scatter(x=daily['date'], y=daily['productivity'], name='Productivity', line=dict(color='green')))
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(df.style.highlight_max(axis=0))
else:
    st.info("No data for the selected period.")