from flask import Flask, render_template, url_for, request, jsonify
import json
import math
import tiles
import tilesSearch
import idastar
from db import helper, handler

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
        
        handler._insert(data)
        
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
        print(req)


        # Heuristic Algo v1
            # array = req.split('#')
            # max = -1

            # for itr in array:
            #     if itr is not "_":
            #         if int(itr) > max:
            #             max = int(itr)

            # rowCount = math.sqrt(max + 1)
            # print(req)
            # result = tilesSearch.search(tiles.TileGame(req, int(rowCount)),req,0)
            # arr = []

            # for i in result :
            #     arr.append(i[2])
            
            # print(arr)

            # return jsonify(arr)

        #IDAStar
        array = req.split("#")
        max = -1

        for itr in range(0,len(array)):
            if array[itr] is not "_":
                if int(array[itr]) > max:
                    max = int(array[itr])
            else:
                array[itr] = "0"
        
        # print("Array", array)
        rowCount = math.sqrt(max + 1)

        for itr in range(0, len(array)):
            array[itr] = int(array[itr])

        logfile = open("test.txt", "w")

        # print("Array", array)
        arr, logarr = idastar.play(tuple(array),int(rowCount), logfile)

        logfile.close()
        print("Solution Array : ", logarr)    
        return jsonify(logarr)



        

@app.route('/getFinalVar', methods = ['POST'])
def get_final_var():
    req = request.get_json()
    global moves, time, retraced, dimension

    moves = req['moves']
    time = req['time']
    retraced = req['retraced']
    dimension = req['dimension']
    print("Moves",moves)
    print("",time)
    print("",retraced)
    return "Received"

@app.route('/success')
def success():
    global user_data, moves, time, retraced, dimension

    handler._update(user_data, moves, time, retraced, dimension)

    return render_template('success.html', moves = moves, time = time)
         

if __name__ == '__main__':
  app.run(debug=True, port=3000)
