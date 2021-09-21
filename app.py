from flask import Flask, render_template, url_for, request, jsonify
import json
import math
import tiles
import tilesSearch
import idastar
from db import helper, handler

app = Flask(__name__,static_folder='static',template_folder='templates')

user_data = {}
num_moves = []
elapsed_time = []
is_solved = []
moves_list = []
image_srcs = []

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
    global user_data, num_moves, elapsed_time, is_solved, moves_list, image_srcs

    num_moves = req['nummoves']
    print("Number of Moves", num_moves)
    elapsed_time = req['elapsedtime']
    is_solved = req['issolved']
    moves_list = req['moveslist']
    image_srcs = req['imagesrc']
    print("Elapsed Time",elapsed_time)
    print("Moves Lists",moves_list)
    print("Images, ", image_srcs)
    handler._update(user_data, num_moves, elapsed_time, is_solved, moves_list, image_srcs)
    return "Received"

@app.route('/success')
def success():
    return render_template('success.html')
         

if __name__ == '__main__':
  app.run(debug=True, port=3000)
