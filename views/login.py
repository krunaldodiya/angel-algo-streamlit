import streamlit as st

from auth import authenticate


def Login():
    st.write("Login")

    secret = st.text_input(label="Secret Key", type="password", key="login_text_input")
    submit = st.button(label="Authenticate", type="primary", key="login_submit_button")

    if submit:
        status = authenticate(secret)

        if status:
            print("auth success")
        else:
            st.write("Login failed. Invalid secret")