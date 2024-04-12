import streamlit as st

from libs.auth import authenticate


def Login():
    try:
        st.title("Login")

        email = st.text_input(label="Email", type="default", key="email_input")
        password = st.text_input(label="Password", type="password", key="password_input")
        submit = st.button(label="Authenticate", type="primary", key="login_submit_button")

        if submit:
            authenticated_user = authenticate(email, password)

            if authenticated_user:
                st.session_state["authenticated_user"] = authenticated_user
                st.rerun()

    except Exception as e:
        st.error("Login failed. Invalid Credentials")