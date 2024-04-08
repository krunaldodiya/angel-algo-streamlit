import pyotp

from typing import Any
from SmartApi import SmartConnect
from SmartApi.smartWebSocketV2 import SmartWebSocketV2
from token_manager.base_token_manager import BaseTokenManager

class AngelOneTokenManager(BaseTokenManager):
    def __init__(
        self,
        client_id: str,
        totp_key: str,
        mpin: str,
        api_key: str,
        api_secret: str,
        redirect_url: str,
    ) -> None:
        super().__init__()

        self.token: str | None = None

        self.client_id = client_id
        self.totp_key = totp_key
        self.mpin = mpin
        self.api_key = api_key
        self.api_secret = api_secret
        self.redirect_url = redirect_url

        self.session = None

        self.http_client = self.get_http_client()

        self.set_access_token_file_name(
            path_name="angel_one_token_manager", unique_id=self.client_id
        )

        self.initialize()


    def get_totp(self, totp_key):
        return pyotp.TOTP(totp_key).now()

    def set_token(self, token: str) -> None:
        self.token = token

    def get_token(self) -> str:
        session = self.get_session()
        token: str = session["jwtToken"]
        return token

    def get_http_client(self) -> SmartConnect:
        try:
            http_client = SmartConnect(self.api_key, timeout=60)

            self.session = http_client.generateSession(
                self.client_id,
                self.mpin,
                self.get_totp(self.totp_key),
            )

            return http_client
        except Exception as e:
            print(e)

    def get_ws_client(self) -> SmartWebSocketV2:
        try:
            ws_client = SmartWebSocketV2(
                self.session['data']["jwtToken"],
                self.api_key,
                self.client_id,
                self.http_client.getfeedToken(),
            )

            return ws_client
        except Exception as e:
            print(e)
