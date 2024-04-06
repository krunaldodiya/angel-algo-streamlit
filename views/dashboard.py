import streamlit as st

from libs.data import load_data, save_data

def Dashboard():
    st.title("Auto Square Off Algo")
    st.write("This tool will auto square off based on MTM")

    # Load existing values from JSON (or set defaults)
    data = load_data()
    stoploss = data.get("stoploss")
    target = data.get("target")

    # Create input fields for stoploss and target
    new_stoploss = st.number_input(label="Stoploss", value=stoploss)
    new_target = st.number_input(label="Target", value=target)

    # Save button to update values
    if st.button("Update"):
        # Update data dictionary with new values
        data["stoploss"] = new_stoploss
        data["target"] = new_target

        # Save updated data to JSON file
        save_data(data)

        # Display success message
        st.success("Stoploss and Target values updated successfully!")

    # Display current stoploss and target values (optional)
    if stoploss is not None and target is not None:
        st.write("Current Stoploss:", stoploss)
        st.write("Current Target:", target)