#  tilesSearch.py
#
#  Search for sequence of moves to bring a randomized tile puzzle
#  into order

import sys, time
from   tiles.tiles  import TileGame
from tiles import sarg


try:
    import Queue as Q  # python ver. < 3.0
except ImportError:
    import queue as Q

def main() :
    board = sys.argv[1]
    ratio = sarg.Int("ratio",2)
    timed = sarg.Int("time",0)
    game  = TileGame(board)
    startTime = time.time()
    path = search(game,board,ratio)
    elapsed = time.time()-startTime
    if timed : timeMsg = "Search took %s secs" % round(elapsed,4)
    else     : timeMsg = ""
    print("tilesSearch.py: Moves=%s %s" % (len(path),timeMsg))
    for entry in path : print(entry)

def search(game, board, ratio) :
    closed  = {}
    queue   = Q.PriorityQueue()
    origCost = game.futureCost(board)*ratio
    orig = (origCost,0,board,None) # (cost,nMoves,board,parent)
    queue.put(orig)
    closed[orig] = True
    expanded = 0
    solution = None
    while queue and not solution :
        parent = queue.get()  
        expanded += 1
        (parCost, parMoves, parBoard, ancester) = parent
        empty, moves = game.getMoves(parBoard)
        for mov in moves :
            childBoard = game.makeMove(parBoard,empty,mov)
            if closed.get(childBoard) : continue
            closed[childBoard] = True
            childMoves = parMoves+1
            childCost = game.futureCost(childBoard)*ratio + childMoves
            child = (childCost,childMoves,childBoard,parent)
            queue.put(child)
            if childBoard == game.goal : solution = child

    if solution :
        print("%s entries expanded. Queue still has %s" % \
             (expanded,                     queue.qsize()))
        # find the path leading to this solution
        path = []
        while solution :
            path.append(solution[0:3]) # drop the parent
            solution = solution[3]     # to grandparent
        path.reverse()
        return path
    else :
        return []

if __name__ == "__main__" : main()
