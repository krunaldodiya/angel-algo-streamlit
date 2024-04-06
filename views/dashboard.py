import streamlit as st

from libs.data import load_data

def Dashboard():
    st.title("Auto Square Off Algo")
    st.write("This tool will auto square off based on MTM")

    # Load existing values from JSON (or set defaults)
    data = load_data()
    stoploss = data.get("stoploss")
    target = data.get("target")

    # Display current stoploss and target values (optional)
    if stoploss is not None and target is not None:
        st.write("Current Stoploss:", stoploss)
        st.write("Current Target:", target)