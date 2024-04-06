import streamlit as st

from libs.auth import authenticate


def Login():
    try:
        st.write("Login")

        email = st.text_input(label="Email", type="default", key="email_input")
        password = st.text_input(label="Password", type="password", key="password_input")
        submit = st.button(label="Authenticate", type="primary", key="login_submit_button")

        if submit:
            authenticate(email, password)
    except Exception as e:
        print(e)
        st.error("Login failed. Invalid Credentials")