import streamlit as st

st.title("⚙️ Settings")
st.write("Model weights configuration (for demo):")
text_w = st.slider("Text weight", 0.0, 1.0, 0.4)
facial_w = st.slider("Facial weight", 0.0, 1.0, 0.3)
speech_w = st.slider("Speech weight", 0.0, 1.0, 0.3)
if st.button("Save Weights"):
    st.session_state['weights'] = (text_w, facial_w, speech_w)
    st.success("Weights updated for aggregation.")