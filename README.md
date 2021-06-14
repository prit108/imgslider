# imgslider

The project aims to implement a [sliding puzzle](https://en.wikipedia.org/wiki/Sliding_puzzle) game, accessed through a web browser.<br/>

## Getting started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Install pip
```bash
python -m pip
```

- Install and create a virtual environment
```bash
pip install virtualenv
python -m venv venv
```

- Install other requirements inside the virtual environment
```bash
source venv/bin/activate
pip install -r requirements.txt
```
### Setting up the database

If you are not familiar with **Firebase** kindly checkout their [official website](https://firebase.google.com) and [docs](https://firebase.google.com/docs).

Since we are using a python wrapper named _**pyrebase**_ you have to setup your own config.py file inside the **db** directory. Kindly checkout the [github repository](https://github.com/thisbejim/Pyrebase). We have also added ```config.py.template``` file to help setting up the credentials. 

If you don't want to do all this, just clone the code from the **heuristic-algo** branch 🙂.

### Starting the server
Run the server with:
```bash
export FLASK_APP=app
flask run
```
The server should be accessible at http://localhost:5000/.

## Play the Game 😁
The game can be played at https://imgsliderv3.herokuapp.com/

For older version (without Auto Solver) check out https://prit108.github.io/imgslider/

⚠️ **Update**: The Auto solver now works on IDA* algorithm instead of the previous heuristic ones. For more details on IDA* check [this](https://en.wikipedia.org/wiki/Iterative_deepening_A*).

⚠️ **Note**: For testing purposes, the current auto solver has been modified to incorporate all the configurations visited in IDA*. Further updates will soon be published.

## About 
✔️ This is a version of the well known Slider-Puzzle, with 2x2, 3x3, 4x4 and 5x5 variants. It has been developed for educational purposes to observe and map   problem solving patterns in human beings.

✔️ The app also includes an A* search solver for 3x3 puzzles that can autosolve any given configuration in optimum number of moves using a heuristic approach.

⚠️ **Coming Soon** : Using Neural Nets, a solver for these puzzles.
