import streamlit as st
import threading

from libs.auth import get_authenticated_user, logout
from tasks.background_task import background_task
from views.dashboard import Dashboard
from views.login import Login
from views.risk_reward import RiskReward
from views.settings import Settings


def start_background_task(authenticated_user):
    # Use a global flag to track if the process is already running
    if not getattr(threading, "background_process_running", False):
        print("starting...")
        thread = threading.Thread(target=background_task, args=(authenticated_user,))
        thread.daemon = True
        thread.start()
        setattr(threading, "background_process_running", True)

if __name__ == "__main__":
    # Authentication and Page Selection
    authenticated_user = get_authenticated_user("main")

    if not authenticated_user:
        page = Login()
    else:
        # Start the background task only once
        start_background_task(authenticated_user)

        st.session_state

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