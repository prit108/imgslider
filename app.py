from flask import Flask, render_template, url_for, request, jsonify
from csv import writer
import json
import math
import re
import base64
from PIL import Image
import numpy as np
import pandas as pd
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
        print("Solution Array : ", arr)    
        return jsonify(arr)



        

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
    handler._update(user_data, moves, time, retraced, dimension)
    return "Received"

@app.route('/success')
def success():
    global user_data, moves, time, retraced, dimension
    return render_template('success.html', moves = moves, time = time)


@app.route('/getImageData', methods = ['POST'])
def imageStitcher():
    json_string = request.get_json()
    req = json_string['images']
    index = json_string['index']
    label = json_string['label']    

    for i in range(9):

        imgstr = re.search(r'base64,(.*)', req[i]).group(1)
        output = open('output' + str(i) + '.png', 'wb')
        output.write(base64.b64decode(imgstr))
        output.close()
    
    img1 = Image.open("output0.png").convert('RGB') 
    img1 = np.array(img1)
    img2 = Image.open("output1.png").convert('RGB') 
    img2 = np.array(img2)
    img3 = Image.open("output2.png").convert('RGB') 
    img3 = np.array(img3)
    img4 = Image.open("output3.png").convert('RGB') 
    img4 = np.array(img4)
    img5 = Image.open("output4.png").convert('RGB') 
    img5 = np.array(img5)
    img6 = Image.open("output5.png").convert('RGB') 
    img6 = np.array(img6)
    img7 = Image.open("output6.png").convert('RGB') 
    img7 = np.array(img7)
    img8 = Image.open("output7.png").convert('RGB') 
    img8 = np.array(img8)
    img9 = Image.open("output8.png").convert('RGB') 
    img9 = np.array(img9)
    print(img1.shape)

    
    #create image of imgg1 array
    imgg1 = np.vstack([np.hstack([img1, img2, img3]) , np.hstack([img4, img5, img6]), np.hstack([img7, img8, img9])]) 
    finalimg1 = Image.fromarray(imgg1)
    #provide the path with name for finalimg1 where you want to save it
    finalimg1.save("images/" + "walkin" + str(index) + ".jpeg")

    data = ["images/" + "walkin" + str(index) + ".jpeg", label]

    with open('sliding_puzzle_data.csv', 'a') as f_object:
  
        writer_object = writer(f_object)

        writer_object.writerow(data)

        f_object.close()

    return "Second image saved"
            

if __name__ == '__main__':

    app.run(debug=True, port=3000)
