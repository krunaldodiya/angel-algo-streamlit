from time import sleep
import streamlit as st

from libs.risk_reward import load_data

def Dashboard():
    st.title("Auto Square Off Algo")
    st.write("This tool will auto square off based on MTM")

    # Load existing values from JSON (or set defaults)
    data = load_data()
    stoploss = data.get("stoploss")
    target = data.get("target")

    # Display current stoploss and target values (optional)
    if stoploss is not None and target is not None:
        st.write(f":red[Stoploss: {stoploss}]")
        st.write(f":green[Target: {target}]")

    if 'pnl' not in st.session_state:
        st.session_state['pnl'] = 0

    pnl_text = st.empty()

    while True:
        pnl_text.text(st.session_state['pnl'])
        sleep(1)