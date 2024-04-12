import streamlit as st

from time import sleep
from libs.auth import get_authenticated_user
from libs.get_running_thread import get_thread
from libs.risk_reward import get_risk_reward
from tasks.background_task import BackgroundTask
from streamlit.runtime.scriptrunner import add_script_run_ctx

def Dashboard():
    st.title("Auto Square Off Algo")
    st.write("This tool will auto square off based on MTM")

    error_text = st.empty()

    st.session_state = {}

    if 'pnl' not in st.session_state:
        st.session_state['pnl'] = 0

    authenticated_user = get_authenticated_user("dashboard")

    thread = get_thread()

    if thread:
        add_script_run_ctx(thread)

    container_2 = st.empty()

    if thread != None:
        start_button = container_2.text("Running")
    else:
        start_button = container_2.button("Start", key="start_button", disabled=False)

    def on_updates(data):
        if 'error' in data:
            error_text.warning(data['error'])

        if 'pnl' in data:
            st.session_state['pnl'] = data['pnl']

    background_task = BackgroundTask()

    if start_button:
        background_task.start_task(authenticated_user['localId'], on_updates)
        container_2.text("Running")

    # Load existing values from JSON (or set defaults)
    stoploss, target = get_risk_reward()

    # Display current stoploss and target values (optional)
    if stoploss is not None and target is not None:
        st.write(f":red[SL: {stoploss}]")
        st.write(f":green[TGT: {target}]")

    pnl_text = st.empty()

    while True:
        pnl = st.session_state['pnl']

        if pnl < 0:
            pnl_text.write(f":red[P&L: {pnl}]")
        elif pnl > 0:
            pnl_text.write(f":green[P&L: {pnl}]")
        else:
            pnl_text.write(f":black[P&L: {pnl}]")

        sleep(1)
