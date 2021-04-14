from flask import Flask, render_template, url_for, request, jsonify
import json
from tiles import tiles
from tiles import tilesSearch
from data import helper

app = Flask(__name__,static_folder='static',template_folder='templates')

user_data = {}
moves = 0
time = ""
retraced = 0
dimension = 0

@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('form.html')
    
    if request.method == 'POST':

        data = helper._jsonifyData(request)        
        
        global user_data

        user_data = data 
        
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
    global moves, time, retraced, dimension

    moves = req['moves']
    time = req['time']
    retraced = req['retraced']
    dimension = req['dimension']
    
    return "Received"

@app.route('/success')
def success():
    global user_data, moves, time, retraced, dimension

    return render_template('success.html', moves = moves, time = time)
         

if __name__ == '__main__':
  app.run(debug=True, port=3000)
