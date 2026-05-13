import streamlit as st
import cv2
from models.facial_emotion import analyze_face
import time
import numpy as np

st.title("🎥 Live Multi‑Modal Detection")

# Webcam live feed with emotion overlay
run = st.checkbox("Start Real‑time Detection")
frame_placeholder = st.empty()
info_placeholder = st.empty()

if run:
    cap = cv2.VideoCapture(0)
    while run:
        ret, frame = cap.read()
        if not ret:
            st.warning("Webcam not accessible.")
            break
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mood, stress, conf = analyze_face(frame)
        cv2.putText(frame, f"Mood: {mood} Stress: {stress:.2f}", (50,50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
        frame_placeholder.image(frame, channels="RGB")
        info_placeholder.metric("Current Mood", mood.capitalize())
        time.sleep(0.1)
    cap.release()