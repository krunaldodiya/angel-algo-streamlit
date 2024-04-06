from token_manager.angel_one_token_manager import AngelOneTokenManager


def validate_token_manager(client_id, totp_key, mpin, api_key, api_secret, redirect_url):
    try:
        token_manager = AngelOneTokenManager(
            client_id=client_id,
            totp_key=totp_key,
            mpin=mpin,
            api_key=api_key,
            api_secret=api_secret,
            redirect_url=redirect_url,
        )

        session = token_manager.get_session()

        profile = token_manager.http_client.getProfile(refreshToken=session["refreshToken"])

        if profile['status']:
            return True
        else:
            return False
    except Exception as e:
        return False