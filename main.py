import streamlit as st

from dotenv import load_dotenv

load_dotenv()

from libs.authenticate import get_authenticated_user, check_cookies_loaded, logout
from views.dashboard import Dashboard
from views.login import Login
from views.risk_reward import RiskReward
from views.settings import Settings

if __name__ == "__main__":
    cookies_loaded = check_cookies_loaded()

    if not cookies_loaded:
        st.write("Please wait...")
    else:
        if "authenticated_user" not in st.session_state:
            st.session_state["authenticated_user"] = get_authenticated_user()

        if 'pnl' not in st.session_state:
            st.session_state['pnl'] = 0

        if 'error' not in st.session_state:
            st.session_state['error'] = ""

        if not st.session_state["authenticated_user"]:
            page = Login()
        else:
            with st.sidebar:
                process_logout = st.button(
                    "Logout",
                    type="primary"
                )

                if process_logout:
                    logout()
                    st.session_state["authenticated_user"] = None
            
            page_selection = st.sidebar.selectbox("Select Page", ["Dashboard", "Risk Reward", "Settings"])

            if page_selection == "Dashboard":
                page = Dashboard()
            elif page_selection == "Settings":
                page = Settings()
            elif page_selection == "Risk Reward":
                page = RiskReward()