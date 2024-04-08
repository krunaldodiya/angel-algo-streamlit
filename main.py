import streamlit as st
import threading

from libs.auth import get_authenticated_user, logout
from token_manager.angel_one_token_manager import AngelOneTokenManager
from views.dashboard import Dashboard
from views.login import Login
from views.risk_reward import RiskReward
from views.settings import Settings

from libs.firebase import db

def async_task(authenticated_user):
    try:
        localId = authenticated_user['localId']

        data = db.child("brokers").child(localId).get().val()

        if not data:
            print("Please add broker info to continue")
        else:
            client_id = data.get("client_id")
            totp_key = data.get("totp_key")
            mpin = data.get("mpin")
            api_key = data.get("api_key")
            api_secret = data.get("api_secret")
            redirect_url = data.get("redirect_url")
        
            token_manager = AngelOneTokenManager(
                client_id=client_id,
                totp_key=totp_key,
                mpin=mpin,
                api_key=api_key,
                api_secret=api_secret,
                redirect_url=redirect_url,
            )

            print(token_manager)
    except Exception as e:
        print("async_task", e)

def start_background_task(authenticated_user):
    # Use a global flag to track if the process is already running
    if not getattr(threading, "background_process_running", False):
        print("starting...")
        thread = threading.Thread(target=async_task, args=(authenticated_user,))
        thread.daemon = True
        thread.start()
        setattr(threading, "background_process_running", True)

if __name__ == "__main__":
    # Authentication and Page Selection
    authenticated_user = get_authenticated_user()

    if not authenticated_user:
        page = Login()
    else:
        # Start the background task only once
        start_background_task(authenticated_user)

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