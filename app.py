from flask import Flask, render_template, url_for, request
import json

app = Flask(__name__,static_folder='static',template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/getInitState', methods = ['POST'])
def get_init_state():
    if request.method == 'POST':
        req =  request.get_json()
        print (req)
        return '', 200        

if __name__ == '__main__':
  app.run(debug=True, port=3000)
