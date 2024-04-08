import streamlit as st
import threading

from libs.auth import get_authenticated_user, logout
from tasks.background_task import background_task
from views.dashboard import Dashboard
from views.login import Login
from views.risk_reward import RiskReward
from views.settings import Settings

from streamlit.runtime.scriptrunner import add_script_run_ctx

pnl_text = st.empty()

def start_background_task(authenticated_user, session_state):
    # Use a global flag to track if the process is already running
    if not getattr(threading, "background_process_running", False):
        print("starting...")
        thread = threading.Thread(target=background_task, args=(authenticated_user, session_state))
        add_script_run_ctx(thread)
        thread.start()
        setattr(threading, "background_process_running", True)
        print("started...")

if __name__ == "__main__":
    # Authentication and Page Selection
    authenticated_user = get_authenticated_user("main")

    if not authenticated_user:
        page = Login()
    else:   
        # Start the background task only once
        start_background_task(authenticated_user, st.session_state)

        with st.sidebar:
            process_logout = st.button(
                "Logout",
                type="primary"
            )

            if process_logout:
                logout()
        
        # User authenticated - Choose between Dashboard and Settings
        page_selection = st.sidebar.selectbox("Select Page", ["Dashboard", "Risk Reward", "Settings"])

        if page_selection == "Dashboard":
            page = Dashboard()
        elif page_selection == "Settings":
            page = Settings()
        elif page_selection == "Risk Reward":
            page = RiskReward()