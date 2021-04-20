from db.handler import _retrieve


def _jsonifyData(request):

    data = {
        "Name" : request.form['name'],
        "Email" : request.form['email'],
        "Phone" : request.form['phone'],
        "Address" : request.form['address'],
        "Age" : request.form['age'],
        "Gender" : request.form['gender'],
        "Profession" : request.form['profession'],
    }

    return data


def _checkEntry(email, profession):

    if _retrieve(email, profession) == None:
        return False
    
    return True

def _findPuzzleData(email, profession):

    user_info = _retrieve(email, profession)

    return user_info['Moves'], user_info['Time taken']

