import streamlit as st

from libs.risk_reward import load_data, save_data

def RiskReward():
    st.title("Risk Reward")

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