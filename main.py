import streamlit as st

from dotenv import load_dotenv

load_dotenv()

from libs.auth import get_authenticated_user, logout
from views.dashboard import Dashboard
from views.login import Login
from views.risk_reward import RiskReward
from views.settings import Settings

if __name__ == "__main__":
    if "authenticated_user" not in st.session_state:
        st.session_state['authenticated_user'] = get_authenticated_user()

    if 'pnl' not in st.session_state:
        st.session_state['pnl'] = 0

    if not st.session_state['authenticated_user']:
        page = Login()
    else:
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