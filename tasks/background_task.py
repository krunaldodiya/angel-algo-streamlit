import threading
from time import sleep

from libs.token_manager import get_token_manager
from streamlit.runtime.scriptrunner import add_script_run_ctx, get_script_run_ctx

class BackgroundTask:
    def __init__(self, authenticated_user, session_state) -> None:
        self.authenticated_user = authenticated_user
        self.session_state = session_state
        self.localId = authenticated_user['localId']

        self.ticks = {}

        self.correlation_id = "abc123"
        self.mode = 1
        self.tokens = []

        self.thread = None
        self.token_manager = None
        self.sws = None

    def start_task(self):
        threads = [thread for thread in threading.enumerate() if thread.name == "background_task"]

        if threads:
            self.thread = threads[0]
        else:
            self.thread = threading.Thread(target=self.background_task, name="background_task")
            add_script_run_ctx(self.thread)
            self.thread.start()

    def stop_task(self):
        if self.sws:
            self.sws.close_connection()

    def background_task(self):
        try:
            self.token_manager = get_token_manager(localId=self.localId)

            position = self.token_manager.http_client.position()

            if not position['data']:
                print("No Positions.")
                return

            for item in position['data']:
                self.tokens.append(item['symboltoken'])

                self.ticks[item['symboltoken']] = {
                    'tradingsymbol': item['tradingsymbol'], 
                    "avgnetprice": float(item['avgnetprice']), 
                    "netqty": int(item['netqty']), 
                    'ltp': float(item['ltp'])
                }

            token_list = [
                {
                    "exchangeType": 2,
                    "tokens": self.tokens
                }
            ]

            def calculate_position_pnl(tick):
                pnl =  tick['ltp'] - tick['avgnetprice'] if tick['netqty'] > 0 else tick['avgnetprice'] - tick['ltp']

                return pnl * abs(tick['netqty'])

            def on_error(wsapp, error):
                print("error", error)

            def on_data(wsapp, data):
                ltp = round(data['last_traded_price'] / 100, 2)
                self.ticks[data['token']]['ltp'] = ltp
                overall_pnl = sum(calculate_position_pnl(tick) for tick in self.ticks.values())
                self.session_state['pnl'] = round(overall_pnl, 2)

            def on_open(wsapp):
                self.sws.subscribe(self.correlation_id, self.mode, token_list)

            self.sws = self.token_manager.get_ws_client()

            self.sws.on_open = on_open
            self.sws.on_data = on_data
            self.sws.on_error = on_error

            self.sws.connect()
        except Exception as e:
            print("background_task", e)