import streamlit as st
import json  # Import json library for file handling

# Define the filename for storing stoploss and target values
DATA_FILE = "stoploss_target.json"


def load_data():
    """Loads stoploss and target values from JSON file (if it exists)."""
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        # Return default values if file doesn't exist
        return {"stoploss": None, "target": None}


def save_data(data):
    """Saves stoploss and target values to JSON file."""
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=2)  # Save with indentation for readability


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
    if st.button("Update Values"):
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