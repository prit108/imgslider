from flask import Flask, render_template, url_for, request, jsonify
import json
import tiles
import tilesSearch

app = Flask(__name__,static_folder='static',template_folder='templates')
moves = 0
time = ""

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
        

@app.route("/form")
def form():
    return render_template("form.html")

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

@app.route('/getFinalVar', methods = ['POST'])
def get_final_var():
    req = request.get_json()
    global moves 
    moves = req['moves']
    global time 
    time = req['time']
    return "Received"

@app.route('/success')
def success():
    return render_template('success.html', moves = moves, time = time)
         

if __name__ == '__main__':
  app.run(debug=True, port=3000)
