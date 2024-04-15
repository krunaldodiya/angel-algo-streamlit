import threading
from time import sleep

from libs.get_running_thread import get_thread
from libs.risk_reward import get_risk_reward
from streamlit.runtime.scriptrunner import add_script_run_ctx

class BackgroundTask:
    def __init__(self, authenticated_user, token_manager) -> None:
        self.authenticated_user = authenticated_user
        self.token_manager = token_manager
        self.sws = None
        self.positions = []
        self.exiting_positions = False

    def start_task(self, token_manager, on_updates):
        thread = get_thread()

        if not thread:
            thread = threading.Thread(target=self.background_task, args=(token_manager, on_updates), name="background_task")
            add_script_run_ctx(thread)
            thread.start()

    def exit_positions(self, message):
        try:
            if not self.positions or self.exiting_positions:
                return
            else:
                print("\n")
                print("message", message)

                self.exiting_positions = True

                positions = self.positions.copy()

                sorted_positions = sorted(positions, key=lambda x: int(x["netqty"]))

                for sorted_position in sorted_positions:
                    netqty = int(sorted_position['netqty'])

                    orderparams = {
                        "variety": "NORMAL",
                        "tradingsymbol": sorted_position['tradingsymbol'],
                        "symboltoken": sorted_position['symboltoken'],
                        "transactiontype": "BUY" if netqty < 0 else "SELL",
                        "exchange": sorted_position['exchange'],
                        "ordertype": "MARKET",
                        "producttype": sorted_position['producttype'],
                        "duration": "DAY",
                        "quantity": abs(netqty),
                    }

                    orderid = self.token_manager.http_client.placeOrder(orderparams)

                    if orderid:
                        print("Order placed with orderid:", orderid)

                self.positions = []
                self.sws.close_connection()
                self.exiting_positions = False
        except Exception as e:
            self.on_updates({'error': str(e)})

    def background_task(self, authenticated_user, token_manager, on_updates):
        try:
            self.authenticated_user = authenticated_user
            self.token_manager = token_manager
            self.on_updates = on_updates
                
            self.correlation_id = "abc123"
            self.mode = 1
            self.tokens = {}

            self.stoploss, self.target = get_risk_reward(authenticated_user['localId'])

            position_query = self.token_manager.http_client.position()

            if position_query['data']:
                self.positions = [position for position in position_query['data'] if int(position['netqty']) != 0]

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
            if not self.positions:
                return
            
            ltp = round(data['last_traded_price'] / 100, 2)
            
            self.tokens[data['token']]['ltp'] = ltp

            overall_pnl = round(sum(calculate_position_pnl(tick) for tick in self.tokens.values()), 2)

            self.on_updates({'pnl': overall_pnl})

            if overall_pnl <= -self.stoploss:
                self.exit_positions("stoploss hit")
            elif overall_pnl >= self.target:
                self.exit_positions("target hit")
            else:
                print("Stoploss", self.stoploss)
                print("Target", self.target)
                print("P&L", overall_pnl)
                print("\n")

        def on_open(wsapp):
            self.sws.subscribe(self.correlation_id, self.mode, token_list)

        self.sws = self.token_manager.get_ws_client()

        self.sws.on_open = on_open
        self.sws.on_data = on_data
        self.sws.on_error = on_error

        self.sws.connect()