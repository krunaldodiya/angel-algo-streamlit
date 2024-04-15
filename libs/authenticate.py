import extra_streamlit_components as stx

from libs.firebase import auth

cookie_manager = stx.CookieManager()

def check_cookies_loaded():
  return cookie_manager.get_all()

def logout():
  cookie_manager.delete("authenticated_user")

def get_authenticated_user():
  try:
      data = cookie_manager.get("authenticated_user")

      if not data:
        return None
      else:
        return data
  except Exception as e:
    return None

def authenticate(email, password):
  user = auth.sign_in_with_email_and_password(email, password)

  if user['idToken'] and user['localId']:
    authenticated_user = {'idToken': user['idToken'], 'localId': user['localId']}

    cookie_manager.set("authenticated_user", authenticated_user)
    
    return authenticated_user
  else:
    return None