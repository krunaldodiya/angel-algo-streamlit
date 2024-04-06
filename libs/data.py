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