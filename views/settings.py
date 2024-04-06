import streamlit as st

def Settings():
    try:
        st.title("Settings")

        email = st.text_input(label="Email", type="default", key="email_input")
        password = st.text_input(label="Password", type="password", key="password_input")
        submit = st.button(label="Authenticate", type="primary", key="login_submit_button")

        if submit:
            print('test')
    except Exception as e:
        st.error("Login failed. Invalid Credentials")