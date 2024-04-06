import extra_streamlit_components as stx

from libs.firebase import auth

cookie_manager = stx.CookieManager(key="cookie-manager")

def is_authenticated():
  token = cookie_manager.get(cookie="token")

  if not token:
    return False
  else:
    return auth.current_user['localId'] == token

def authenticate(email, password):
  user = auth.sign_in_with_email_and_password(email, password)

  if user['localId']:
    cookie_manager.set(cookie="token", val=user['localId'])