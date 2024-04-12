import os
import pyrebase

config = {
  "apiKey": os.getenv("API_KEY"),
  "authDomain": os.getenv("AUTH_DOMAIN"),
  "databaseURL": os.getenv("DATABASE_URL"),
  "storageBucket": os.getenv("STORAGE_BUCKET"),
}

firebase = pyrebase.initialize_app(config)

auth = firebase.auth()

db = firebase.database()
