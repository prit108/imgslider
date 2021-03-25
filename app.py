from flask import Flask, render_template, url_for

app = Flask(__name__,static_folder='static',template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
  app.run(debug=True, port=3000)
