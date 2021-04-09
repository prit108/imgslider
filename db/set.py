import pyrebase
from config import firebaseConfig

firebase = pyrebase.initialize_app(firebaseConfig)

def _setDatabase():
    
    db = firebase.database()
    return db