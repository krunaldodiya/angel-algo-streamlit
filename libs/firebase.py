import pyrebase

config = {
  "apiKey": "AIzaSyACnXQ-QV1tmBvCLKFvbRaOhEITUYcciA4",
  "authDomain": "angelalgo-5029f.firebaseapp.com",
  "databaseURL": "https://angelalgo-5029f-default-rtdb.firebaseio.com",
  "storageBucket": "angelalgo-5029f.appspot.com"
}

firebase = pyrebase.initialize_app(config)

auth = firebase.auth()

db = firebase.database()
