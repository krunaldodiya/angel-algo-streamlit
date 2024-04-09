import threading

from time import sleep
from libs.token_manager import get_token_manager
from streamlit.runtime.scriptrunner import add_script_run_ctx

class BackgroundTask:
    def __init__(self, authenticated_user, session_state) -> None:
        self.authenticated_user = authenticated_user
        self.session_state = session_state
        self.localId = authenticated_user['localId']
        self.ticks = {}
        self.tokens = []

    def run_thread(self):
        if not getattr(threading, "background_process_running", False):
            print("starting...")
            thread = threading.Thread(target=self.background_task)
            add_script_run_ctx(thread)
            thread.start()

    def background_task(self):
        try:
            token_manager = get_token_manager(localId=self.localId)

            # position = token_manager.http_client.position()

            # while True:
            #     if position:
            #         break
            #     else:
            #         print("No Positions yet")
            #         sleep(1)

            # for item in position['data']:
            #     self.tokens.append(item['symboltoken'])

            #     self.ticks[item['symboltoken']] = {
            #         'tradingsymbol': item['tradingsymbol'], 
            #         "avgnetprice": float(item['avgnetprice']), 
            #         "netqty": int(item['netqty']), 
            #         'ltp': float(item['ltp'])
            #     }
            
            # correlation_id = "abc123"
            # mode = 1
            # token_list = [
            #     {
            #         "exchangeType": 2,
            #         "tokens": self.tokens
            #     }
            # ]

            # sws = token_manager.get_ws_client()

            # def calculate_position_pnl(tick):
            #     pnl =  tick['ltp'] - tick['avgnetprice'] if tick['netqty'] > 0 else tick['avgnetprice'] - tick['ltp']

            #     return pnl * abs(tick['netqty'])

            # def on_error(wsapp, error):
            #     print("error", error)

            # def on_data(wsapp, data):
            #     ltp = round(data['last_traded_price'] / 100, 2)
            #     self.ticks[data['token']]['ltp'] = ltp
            #     overall_pnl = sum(calculate_position_pnl(tick) for tick in self.ticks.values())
            #     self.session_state['pnl'] = round(overall_pnl, 2)

            # def on_open(wsapp):
            #     setattr(threading, "background_process_running", True)
            #     print("started...")
            #     sws.subscribe(correlation_id, mode, token_list)
            #     print("subscribed...")

            # sws.on_open = on_open
            # sws.on_data = on_data
            # sws.on_error = on_error

            # sws.connect()
        except Exception as e:
            print("background_task", e)