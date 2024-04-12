import threading


def get_thread():
    threads = [thread for thread in threading.enumerate() if thread.name == "background_task"]

    if threads:
        return threads[0]
    else:
        return None