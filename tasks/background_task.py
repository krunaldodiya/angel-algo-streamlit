from time import sleep
from libs.token_manager import get_token_manager

def background_task(authenticated_user):
    ticks = {}

    tokens = []

    try:
        localId = authenticated_user['localId']

        token_manager = get_token_manager(localId=localId)

        if not token_manager:
            print("Failed to fetch broker details")
            return
        
        position = token_manager.http_client.position()

        if not position:
            print("No Positions")
            return
        
        for item in position['data']:
            tokens.append(item['symboltoken'])
            ticks[item['symboltoken']] = {'tradingsymbol': item['tradingsymbol'], 'ltp': item['ltp']}

        sws = token_manager.get_ws_client()

        def on_data(wsapp, data):
            ltp = round(data['last_traded_price'] / 100, 2)
            ticks[data['token']]['ltp'] = ltp

            print(ticks)

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

        sws.connect()
    except Exception as e:
        print("background_task", e)