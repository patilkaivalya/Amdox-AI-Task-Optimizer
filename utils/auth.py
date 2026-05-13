import streamlit as st
from utils.database import get_session, Employee

def check_login(username, password):
    session = get_session()
    user = session.query(Employee).filter_by(username=username, password=password).first()
    session.close()
    return user

def init_session():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.user = None
        st.session_state.role = None
        st.session_state.emp_id = None
        st.session_state.name = None