import streamlit as st

from time import sleep
from libs.get_running_thread import get_thread
from libs.risk_reward import get_risk_reward
from libs.token_manager import get_token_manager
from tasks.background_task import BackgroundTask
from streamlit.runtime.scriptrunner import add_script_run_ctx

def Dashboard():
    st.title("Auto Square Off Algo")
    st.write("This tool will auto square off based on MTM")

    authenticated_user = st.session_state["authenticated_user"]

    thread = get_thread()

    if thread:
        add_script_run_ctx(thread)

    if 'thread_status' not in st.session_state:
        st.session_state['thread_running'] = thread != None

    container_2 = st.empty()

    if st.session_state['thread_running']:
        start_button = container_2.text("Running")
    else:
        start_button = container_2.button("Start", key="start_button")

    error_text = st.empty()

    def on_updates(data):
        if 'error' in data:
            st.session_state['error'] = data['error']
            error_text.warning(data['error'])

        if 'pnl' in data:
            st.session_state['pnl'] = data['pnl']

    if start_button:
        token_manager = get_token_manager(authenticated_user)

        if token_manager:
            background_task = BackgroundTask(authenticated_user, token_manager)
            background_task.start_task(on_updates)
            container_2.text("Running")
            st.session_state['thread_running'] = 'running'

        # Load existing values from JSON (or set defaults)
        stoploss, target = get_risk_reward(authenticated_user['localId'])

        # Display current stoploss and target values (optional)
        if stoploss is not None and target is not None:
            st.write(f":red[SL: {stoploss}]")
            st.write(f":green[TGT: {target}]")

        pnl_text = st.empty()

        if st.session_state['thread_running']:
            while True:
                pnl = st.session_state['pnl']

                if pnl < 0:
                    pnl_text.write(f":red[P&L: {pnl}]")
                elif pnl > 0:
                    pnl_text.write(f":green[P&L: {pnl}]")
                else:
                    pnl_text.write(f":black[P&L: {pnl}]")

                sleep(1)
