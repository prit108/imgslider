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