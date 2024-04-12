import threading

from libs.get_running_thread import get_thread
from libs.risk_reward import load_data
from libs.token_manager import get_token_manager
from streamlit.runtime.scriptrunner import add_script_run_ctx

class BackgroundTask:
    def __init__(self) -> None:
        self.thread = get_thread()

    def start_task(self, localId, on_updates):
        if not self.thread:
            self.thread = threading.Thread(target=self.background_task, args=(localId, on_updates), name="background_task")
    
        add_script_run_ctx(self.thread)

        self.thread.start()

    def stop_task(self):
        if self.sws:
            self.sws.close_connection()

    def exit_positions(self, message):
        print(message)

    def background_task(self, localId, on_updates):
        try:
            self.localId = localId
            self.on_updates = on_updates
                
            self.correlation_id = "abc123"
            self.mode = 1
            self.tokens = {}

            self.token_manager = None
            self.sws = None

            data = load_data()

            self.stoploss = data.get("stoploss")
            self.target = data.get("target")

            self.positions = []

            self.token_manager = get_token_manager(localId=self.localId)

            position_query = self.token_manager.http_client.position()

            if position_query['data']:
                self.positions = position_query['data']

            if self.positions:
                self.manage_positions()
            else:
                self.on_updates({'error': 'No Positions.'})
        except Exception as e:
            self.on_updates({'error': str(e)})
    
    def manage_positions(self):
        for item in self.positions:
            token = item['symboltoken']

            self.tokens[token] = {
                'tradingsymbol': item['tradingsymbol'], 
                "avgnetprice": float(item['avgnetprice']), 
                "netqty": int(item['netqty']), 
                'ltp': float(item['ltp'])
            }

        token_list = [
            {
                "exchangeType": 2,
                "tokens": [token for token in self.tokens.keys()]
            }
        ]

        def calculate_position_pnl(tick):
            pnl =  tick['ltp'] - tick['avgnetprice'] if tick['netqty'] > 0 else tick['avgnetprice'] - tick['ltp']

            return pnl * abs(tick['netqty'])

        def on_error(wsapp, error):
            print("error", error)

        def on_data(wsapp, data):
            ltp = round(data['last_traded_price'] / 100, 2)
            
            self.tokens[data['token']]['ltp'] = ltp
            
            overall_pnl = sum(calculate_position_pnl(tick) for tick in self.tokens.values())

            self.on_updates({'pnl': round(overall_pnl, 2)})

            if overall_pnl <= -self.stoploss:
                self.exit_positions("stoploss hit")
            elif overall_pnl >= self.target:
                self.exit_positions("target hit")
            else:
                print("overall_pnl", overall_pnl)
                print("stoploss", self.stoploss)
                print("target", self.target)
                print("\n")

        def on_open(wsapp):
            self.sws.subscribe(self.correlation_id, self.mode, token_list)

        self.sws = self.token_manager.get_ws_client()

        self.sws.on_open = on_open
        self.sws.on_data = on_data
        self.sws.on_error = on_error

        self.sws.connect()