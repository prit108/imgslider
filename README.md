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

### Starting the server
Run the server with:
```bash
flask run
```
The API server should be accessible at http://localhost:5000/.

## Play the Game 😁
The game can be played at https://imgslider.herokuapp.com/
For older version (without Auto Solver) check out https://prit108.github.io/imgslider/

## About 
✔️ This is a version of the well known Slider-Puzzle, with 2x2, 3x3, 4x4 and 5x5 variants. It has been developed for educational purposes to observe and map   problem solving patterns in human beings.

✔️ The app also includes an A* search solver for 3x3 puzzles that can autosolve any given configuration in optimum number of moves using a heuristic approach.

✔️ Coming Soon : 
      ⚡ Algorithmic Solvers for other sizes. 
      ⚡ Using Neural Nets for these puzzles.
