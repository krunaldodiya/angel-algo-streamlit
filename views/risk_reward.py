import streamlit as st

from libs.firebase import db
from libs.risk_reward import get_risk_reward

def RiskReward():
    st.title("Risk Reward")

    authenticated_user = st.session_state["authenticated_user"]

    localId = authenticated_user['localId']

    stoploss, target = get_risk_reward(localId)

    # Create input fields for stoploss and target
    new_stoploss = st.number_input(label="Stoploss", value=stoploss)
    new_target = st.number_input(label="Target", value=target)

    # Save button to update values
    if st.button("Update"):
        db.child("risk_reward").child(localId).set({
            "stoploss": new_stoploss,
            "target": new_target,
        })

        # Display success message
        st.success("Stoploss and Target values updated successfully!")