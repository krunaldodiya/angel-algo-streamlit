from streamlit_local_storage import LocalStorage

from libs.firebase import auth

local_storage = LocalStorage()

def logout():
  local_storage.deleteItem("authenticated_user")

def get_authenticated_user():
  data = local_storage.getItem("authenticated_user")

  if not data:
    return None

  return data["authenticated_user"]

def authenticate(email, password):
  user = auth.sign_in_with_email_and_password(email, password)

  if user['idToken'] and user['localId']:
    authenticated_user = {'idToken': user['idToken'], 'localId': user['localId']}

    local_storage.setItem("authenticated_user", authenticated_user)
    
    return authenticated_user
  else:
    return None