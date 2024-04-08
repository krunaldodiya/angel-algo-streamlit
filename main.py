import streamlit as st
from libs.auth import get_authenticated_user, logout
from views.dashboard import Dashboard
from views.login import Login
from views.risk_reward import RiskReward
from views.settings import Settings


if __name__ == "__main__":
    # Authentication and Page Selection
    authenticated_user = get_authenticated_user("main")

    if not authenticated_user:
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