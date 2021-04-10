import pyrebase
import random
from db.config import firebaseConfig

firebase = pyrebase.initialize_app(firebaseConfig)

db = firebase.database()
auth = firebase.auth()
key = ""

def _insert(data):
    global db, key
    key = str(random.randint(0,1e9))
    print("This is the mf key : " , key)
    db.child(data['Profession'].lower()).child(key).set(data)

def _remove(data):
    global db, key
    db.child(data['Profession'].lower()).child(key).remove()

def _retrieve(data):
    global db, key
    user = db.child(data['Profession'].lower()).child(key).get()

    return user

def _update(data, moves, time, retraced, dimension):
    global db, key
    db.child(data['Profession'].lower()).child(key).update({'Moves' : moves, 'Time taken' : time, 'Retraced Moves' : retraced, 'Dimension' : dimension})