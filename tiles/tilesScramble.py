#  tilesScramble.py
#
#  Scramble the solution by making N random moves.

def scramble(times) :
    import tiles, random
    board = "12345678_"
    game = tiles.TileGame(board) # the goal board
    used = {}
    while times > 0 :
        used[board] = True             # mark as taken
        empty, moves = game.getMoves(board)
        move = random.choice(moves)
        nextBoard = game.makeMove(board,empty,move)
        if used.get(nextBoard) : continue
        board = nextBoard
        times -= 1
    return board

def main() :
    import sys, sarg
    moves = sarg.Int("moves",15)   # Number of times to randomly move
    print(scramble(moves))

if __name__ == "__main__" : main()
