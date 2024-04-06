import streamlit as st
import threading

from libs.auth import is_authenticated
from token_manager.angel_one_token_manager import AngelOneTokenManager
from views.dashboard import Dashboard
from views.login import Login
from views.risk_reward import RiskReward
from views.settings import Settings

from libs.firebase import auth, db

def async_task():
    try:
        localId = auth.current_user['localId']

        data = db.child("brokers").child(localId).get().val()

        if data:
            token_manager = AngelOneTokenManager(
                client_id=data.get("client_id"),
                totp_key=data.get("totp_key"),
                mpin=data.get("mpin"),
                api_key=data.get("api_key"),
                api_secret=data.get("api_secret"),
                redirect_url=data.get("redirect_url"),
            )

            print(token_manager)
    except Exception as e:
        print(e)

def start_background_task():
    # Use a global flag to track if the process is already running
    if not getattr(threading, "background_process_running", False):
        print("starting...")
        thread = threading.Thread(target=async_task)
        thread.daemon = True
        thread.start()
        setattr(threading, "background_process_running", True)

if __name__ == "__main__":
    # Authentication and Page Selection
    authenticated = is_authenticated()

    if not authenticated:
        page = Login()
    else:    
        # Start the background task only once
        start_background_task()
        
        # User authenticated - Choose between Dashboard and Settings
        page_selection = st.sidebar.selectbox("Select Page", ["Dashboard", "Risk Reward", "Settings"])

        if page_selection == "Dashboard":
            page = Dashboard()
        elif page_selection == "Settings":
            page = Settings()
        elif page_selection == "Risk Reward":
            page = RiskReward()