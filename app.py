from flask import Flask, render_template, url_for, request, jsonify
import json
import tiles
import tilesSearch

app = Flask(__name__,static_folder='static',template_folder='templates')

@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('form.html')
    
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        address = request.form['address']
        age = request.form['age']
        gender = request.form['gender']
        profession = request.form['profession']
        print(name,phone,address,age,gender,profession)
        return render_template('index.html')
        

@app.route('/getInitState', methods = ['GET', 'POST'])
def get_init_state():
    if request.method == 'POST':
        req =  request.get_json()

        result = tilesSearch.search(tiles.TileGame(req),req,0)
        arr = []

        for i in result :
            arr.append(i[2])
        
        print(arr)

        return jsonify(arr)

@app.route('/success')
def success():
    return render_template('index.html')
         

if __name__ == '__main__':
  app.run(debug=True, port=3000)
