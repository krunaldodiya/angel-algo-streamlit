import pyrebase

config = {
  "apiKey": "AIzaSyACnXQ-QV1tmBvCLKFvbRaOhEITUYcciA4",
  "authDomain": "angel-algo-streamlit.firebaseapp.com",
  "databaseURL": "https://angel-algo-streamlit-default-rtdb.firebaseio.com",
  "storageBucket": "angel-algo-streamlit.appspot.com",
  "appId": "1:572283903883:web:4906eccab4f9fa3872198e"
}

firebase = pyrebase.initialize_app(config)