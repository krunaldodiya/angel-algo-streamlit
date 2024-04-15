from token_manager.angel_one_token_manager import AngelOneTokenManager
from libs.firebase import db

def get_token_manager(authenticated_user):
    try:
        data = db.child("brokers").child(authenticated_user['localId']).get().val()

        if not data:
            return None
        else:
            client_id = data.get("client_id")
            totp_key = data.get("totp_key")
            mpin = data.get("mpin")
            api_key = data.get("api_key")
            api_secret = data.get("api_secret")
            redirect_url = data.get("redirect_url")

            return validate_token_manager(
                client_id, totp_key, mpin, api_key, api_secret, redirect_url
            )
    except Exception as e:
        print("get_token_manager", e)
        return None

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

        profile = token_manager.http_client.getProfile(refreshToken=token_manager.session["data"]["refreshToken"])

        if profile['status']:
            return token_manager
        else:
            return None
    except Exception as e:
        print("validate_token_manager", e)
        return None