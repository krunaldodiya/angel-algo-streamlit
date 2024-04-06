import extra_streamlit_components as stx

from libs import firebase

cookie_manager = stx.CookieManager()

def is_authenticated():
  token = cookie_manager.get(cookie="token")

  if not token:
    return False
  else:
    return True

def authenticate(email, password):
  auth = firebase.firebase.auth()
  user = auth.sign_in_with_email_and_password(email, password)
  
  if user['localId']:
    cookie_manager.set("token", user['localId'])