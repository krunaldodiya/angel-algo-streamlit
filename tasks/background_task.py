from libs.token_manager import get_token_manager

def background_task(authenticated_user):
    try:
        localId = authenticated_user['localId']

        token_manager = get_token_manager(localId=localId)

        if not token_manager:
            print("Failed to fetch broker details")
        else:
            profile = token_manager.http_client.getProfile(refreshToken=token_manager.session['data']['refreshToken'])
            print("profile", profile)
    except Exception as e:
        print("async_task", e)