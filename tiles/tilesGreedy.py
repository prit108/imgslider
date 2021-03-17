#  tilesGreedy.py
#
#  Advance with only the best choice at each move. Toss the others

import sys, time, sarg
from tiles import TileGame

def search(game, board) :
    path    = []
    closed  = {}         # boards already seen
    closed[board] = True # don't return (avoid loops)
    while True :
        path.append(board)
        if board == game.goal : break
        empty, moves = game.getMoves(board)
        candidates = []
        for mov in moves :
            child = game.makeMove(board,empty,mov)
            priority = game.futureCost(child)
            if not closed.get(child) :
                candidates.append( (priority,child) )
                closed[child] = True
        if candidates :
            candidates.sort()
            board = candidates[0][1]  # choose lowest cost board for next
        else :
            print("Cannot move from %s" % board)
            break
    return path

def main() :
    board = sys.argv[1]     # board is a 9 or 16 digit board
    timed = sarg.Int("time",0)
    game  = TileGame(board)

    startTime = time.time()
    path = search(game, board)
    elapsed = time.time()-startTime
    if timed : timeMsg = "Search took %s secs" % round(elapsed,4)
    else     : timeMsg = ""
    print("tilesGreedy.py: %s moves=%s %s" % (board,len(path),timeMsg))
    for entry in path[:30] : print(entry)
    if len(path) > 30 : print("...")

if __name__ == "__main__" : main()
