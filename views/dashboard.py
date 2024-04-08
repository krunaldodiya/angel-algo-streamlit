import streamlit as st

import threading

from libs.auth import get_authenticated_user
from tasks.background_task import background_task
from streamlit.runtime.scriptrunner import add_script_run_ctx
from time import sleep
from libs.risk_reward import load_data

def run_thread(authenticated_user, session_state):
    # Use a global flag to track if the process is already running
    if not getattr(threading, "background_process_running", False):
        print("starting...")
        thread = threading.Thread(target=background_task, args=(authenticated_user, session_state))
        add_script_run_ctx(thread)
        thread.start()
        setattr(threading, "background_process_running", True)
        print("started...")

def Dashboard():
    st.title("Auto Square Off Algo")
    st.write("This tool will auto square off based on MTM")

    authenticated_user = get_authenticated_user("dashboard")

    thread_button = st.button("Start")

    if thread_button:
        run_thread(authenticated_user, st.session_state)

    # Load existing values from JSON (or set defaults)
    data = load_data()
    stoploss = data.get("stoploss")
    target = data.get("target")

    # Display current stoploss and target values (optional)
    if stoploss is not None and target is not None:
        st.write(f":red[SL: {stoploss}]")
        st.write(f":green[TGT: {target}]")

    if 'pnl' not in st.session_state:
        st.session_state['pnl'] = 0

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