import streamlit as st

from libs.auth import get_authenticated_user
from libs.token_manager import validate_token_manager
from libs.firebase import db

def Settings():
    try:
        st.title("Settings")

        authenticated_user = get_authenticated_user("settings")

        localId = authenticated_user['localId']

        data = db.child("brokers").child(localId).get().val()
        
        if data:
            client_id = data.get("client_id")
            totp_key = data.get("totp_key")
            mpin = data.get("mpin")
            api_key = data.get("api_key")
            api_secret = data.get("api_secret")
            redirect_url = data.get("redirect_url")
        else:
            client_id = ""
            totp_key = ""
            mpin = ""
            api_key = ""
            api_secret = ""
            redirect_url = ""

        client_id = st.text_input(label="Client ID", type="default", key="client_id_input", value=client_id)
        totp_key = st.text_input(label="TOTP Key", type="password", key="totp_key_input", value=totp_key)
        mpin = st.text_input(label="MPIN", type="password", key="mpin_input", value=mpin)
        api_key = st.text_input(label="API Key", type="default", key="api_key_input", value=api_key)
        api_secret = st.text_input(label="API Secret", type="password", key="api_secret_input", value=api_secret)
        redirect_url = st.text_input(label="Redirect URL", type="default", key="redirect_url_input", value=redirect_url)
        submit = st.button(label="Update", type="primary", key="login_submit_button")

        if submit:
            is_valid_api_details = validate_token_manager(
                client_id, totp_key, mpin, api_key, api_secret, redirect_url
            )

            if not is_valid_api_details:
                st.error("Invalid API Details.")
            else:
                db.child("brokers").child(localId).set({
                    "client_id":client_id,
                    "totp_key":totp_key,
                    "mpin":mpin,
                    "api_key":api_key,
                    "api_secret":api_secret,
                    "redirect_url":redirect_url
                })

                st.success("Updated Successfully.")
    except Exception as e:
        st.error(e)