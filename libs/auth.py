from streamlit_local_storage import LocalStorage

from libs.firebase import auth

local_storage = LocalStorage()

def logout():
  local_storage.deleteItem("auth")

def get_authenticated_user(page):
  data = local_storage.getItem("auth", key=page)

  if not data:
    return None

  return data['auth']

def authenticate(email, password):
  user = auth.sign_in_with_email_and_password(email, password)

  if user['idToken'] and user['localId']:
    local_storage.setItem("auth", {'idToken': user['idToken'], 'localId': user['localId']})