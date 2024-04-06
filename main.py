import threading

from datetime import datetime
from time import sleep
from libs.auth import is_authenticated
from views.dashboard import Dashboard
from views.login import Login

def async_task():
    while True:
        # Your square-off logic goes here
        print("datetime", datetime.now())
        sleep(1)  # Replace with your desired sleep time


def start_background_task():
    # Use a global flag to track if the process is already running
    if not getattr(threading, "background_process_running", False):
        print("starting...")
        thread = threading.Thread(target=async_task)
        thread.daemon = True
        thread.start()
        setattr(threading, "background_process_running", True)

if __name__ == "__main__":
    # Start the background task only once
    start_background_task()

    authenticated = is_authenticated()

    if authenticated:
        Dashboard()
    else:
        Login()
