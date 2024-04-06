import extra_streamlit_components as stx

cookie_manager = stx.CookieManager()

SECRET = 'test'

def is_authenticated():
  token = cookie_manager.get(cookie="token")

  if not token:
    return False
  else:
    return True

def authenticate(secret):
  if secret == SECRET:
    cookie_manager.set("token", SECRET)
    return True
  else:
    return False