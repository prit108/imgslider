from flask import Flask, render_template, url_for, request, jsonify
import json
import tiles
import tilesSearch

app = Flask(__name__,static_folder='static',template_folder='templates')

@app.route('/')
def index():
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

if __name__ == '__main__':
  app.run(debug=True, port=3000)
