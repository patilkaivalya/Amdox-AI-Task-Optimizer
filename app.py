import streamlit as st
from utils.auth import init_session, check_login
from utils.database import get_session, Employee
import streamlit.components.v1 as components

st.set_page_config(page_title="Amdox AI Task Optimizer", layout="wide",
                   page_icon="🧠", initial_sidebar_state="expanded")

# Load custom CSS
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

init_session()

def login_ui():
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("<div class='login-card'>", unsafe_allow_html=True)
        st.image("https://img.icons8.com/fluency/96/brain.png", width=80)
        st.markdown("<h2 style='text-align:center;'>Amdox AI Task Optimizer</h2>", unsafe_allow_html=True)
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login", use_container_width=True):
            user = check_login(username, password)
            if user:
                st.session_state.logged_in = True
                st.session_state.user = user.username
                st.session_state.role = user.role
                st.session_state.emp_id = user.id
                st.session_state.name = user.name
                st.rerun()
            else:
                st.error("Invalid credentials")
        st.markdown("</div>", unsafe_allow_html=True)

def main_app():
    if st.session_state.role == 'employee':
        pages = {
            "Employee Dashboard": "pages/1_Employee_Dashboard.py",
            "Real‑time Detection": "pages/3_Real_Time_Detection.py",
            "Analytics": "pages/4_Analytics.py",
            "Settings": "pages/5_Settings.py"
        }
    else:
        pages = {
            "HR Dashboard": "pages/2_HR_Dashboard.py",
            "Analytics": "pages/4_Analytics.py",
            "Settings": "pages/5_Settings.py"
        }

    st.sidebar.title(f"Welcome, {st.session_state.name}")
    st.sidebar.markdown(f"Role: **{st.session_state.role.upper()}**")
    if st.sidebar.button("Logout"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

    # Navigation
    choice = st.sidebar.radio("Navigate", list(pages.keys()))
    # Load the selected page
    exec(open(pages[choice]).read())

if not st.session_state.logged_in:
    login_ui()
else:
    main_app()