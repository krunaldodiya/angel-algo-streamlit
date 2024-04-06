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

        http_client = token_manager.get_http_client()

        print("http_client", http_client)

        userProfile = http_client.getProfile()

        print(userProfile)

        if userProfile:
            return True
        else:
            return False
    except Exception as e:
        return False