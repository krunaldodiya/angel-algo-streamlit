from time import sleep
from libs.token_manager import get_token_manager

def background_task(authenticated_user):
    ticks = {}

    tokens = []

    try:
        localId = authenticated_user['localId']

        token_manager = get_token_manager(localId=localId)

        if not token_manager.http_client:
            print("Failed to fetch broker details")
            return
        
        position = token_manager.http_client.position()

        if not position:
            print("No Positions")
            return
        
        for item in position['data']:
            tokens.append(item['symboltoken'])

            ticks[item['symboltoken']] = {
                'tradingsymbol': item['tradingsymbol'], 
                "avgnetprice": float(item['avgnetprice']), 
                "netqty": int(item['netqty']), 
                'ltp': float(item['ltp'])
            }

        sws = token_manager.get_ws_client()

        def calculate_position_pnl(tick):
            pnl =  tick['ltp'] - tick['avgnetprice'] if tick['netqty'] > 0 else tick['avgnetprice'] - tick['ltp']

            return pnl * abs(tick['netqty'])

        def on_error(wsapp, error):
            print("error", error)

        def on_data(wsapp, data):
            ltp = round(data['last_traded_price'] / 100, 2)
            
            ticks[data['token']]['ltp'] = ltp

            overall_pnl = sum(calculate_position_pnl(tick) for tick in ticks.values())

            print("overall_pnl", round(overall_pnl, 2))

        def on_open(wsapp):
            correlation_id = "abc123"
            mode = 1
            token_list = [
                {
                    "exchangeType": 2,
                    "tokens": tokens
                }
            ]

            sws.subscribe(correlation_id, mode, token_list)

        sws.on_open = on_open
        sws.on_data = on_data
        sws.on_error = on_error

        sws.connect()
    except Exception as e:
        print("background_task", e)