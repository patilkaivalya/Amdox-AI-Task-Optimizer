import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from utils.database import get_employee_moods, add_mood_record
from models.text_emotion import analyze_text
from models.facial_emotion import analyze_face
from models.speech_emotion import analyze_speech
from models.recommendation_model import recommend_task
from utils.alert_system import check_stress_alerts
import cv2
import numpy as np
from PIL import Image

st.title("🧑‍💼 Employee Dashboard")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("<div class='mood-card'>", unsafe_allow_html=True)
    st.subheader("📝 Text Mood Input")
    text = st.text_area("How are you feeling?", "I'm feeling great today!")
    if st.button("Analyze Text"):
        mood, stress, conf = analyze_text(text)
        st.session_state['text_mood'] = mood
        st.session_state['text_stress'] = stress
        st.success(f"Mood: {mood} (stress: {stress:.2f})")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='mood-card'>", unsafe_allow_html=True)
    st.subheader("📷 Facial Emotion")
    run_cam = st.checkbox("Start webcam")
    if run_cam:
        img_placeholder = st.empty()
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        if ret:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mood, stress, conf = analyze_face(frame_rgb)
            img_placeholder.image(frame_rgb, channels="RGB")
            st.session_state['facial_mood'] = mood
            st.session_state['facial_stress'] = stress
        cap.release()
    st.markdown("</div>", unsafe_allow_html=True)

with col3:
    st.markdown("<div class='mood-card'>", unsafe_allow_html=True)
    st.subheader("🎤 Speech Emotion")
    if st.button("Record (5 sec) & Analyze"):
        with st.spinner("Recording..."):
            mood, stress, conf = analyze_speech()
            st.session_state['speech_mood'] = mood
            st.session_state['speech_stress'] = stress
            st.success(f"Speech mood: {mood}")
    st.markdown("</div>", unsafe_allow_html=True)

# Combine moods
if 'text_mood' in st.session_state and 'facial_mood' in st.session_state and 'speech_mood' in st.session_state:
    moods = [st.session_state.text_mood, st.session_state.facial_mood, st.session_state.speech_mood]
    stress_vals = [st.session_state.text_stress, st.session_state.facial_stress, st.session_state.speech_stress]
    # Weighted average stress
    final_stress = np.average(stress_vals, weights=[0.4, 0.3, 0.3])
    # Simple voting for mood (most frequent)
    from collections import Counter
    final_mood = Counter(moods).most_common(1)[0][0]
    st.markdown("---")
    st.subheader("🧠 Final Aggregated Analysis")
    colA, colB = st.columns(2)
    colA.metric("Mood", final_mood.capitalize())
    colB.metric("Stress Level", f"{final_stress:.2f}", delta=None)
    productivity = 0.8 if final_mood in ['happy','focused'] else 0.5
    rec_task = recommend_task(final_mood, final_stress, productivity)
    st.info(f"Recommended Task: **{rec_task}**")

    if st.button("Save & Proceed"):
        add_mood_record(st.session_state.emp_id,
                        st.session_state.text_mood,
                        st.session_state.facial_mood,
                        st.session_state.speech_mood,
                        final_mood, final_stress, productivity, rec_task)
        check_stress_alerts(st.session_state.emp_id)
        st.success("Mood record saved!")

# Historical chart
st.markdown("---")
st.subheader("📊 Your Mood Timeline (Last 7 Days)")
records = get_employee_moods(st.session_state.emp_id, days=7)
if records:
    df = pd.DataFrame([{
        'timestamp': r.timestamp,
        'mood': r.final_mood,
        'stress': r.stress_level
    } for r in records])
    fig = px.line(df, x='timestamp', y='stress', color='mood', markers=True)
    st.plotly_chart(fig, use_container_width=True)