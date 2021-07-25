# tiles.py
#
import sys

class TileGame :
    def __init__ (self, sampleBoard, rowCount) :
        self.legalMoves = legalString(rowCount)
        self.goal       = goalExpr(rowCount)
        self.dim        = rowCount   
        self.makeManhatten()

    def getMoves(self, board) :
        array = board.split('#')
        empty = findEmpty(array)
        return empty, self.legalMoves[empty]
    
    def makeMove(self, board, empty, mov) :
        lbrd = board.split('#')
        lbrd[empty],lbrd[mov] = lbrd[mov],lbrd[empty]

        temp = ""
        for i in lbrd:
            temp += i + "#"
        return temp[0:len(temp)-1]
    
    def futureCost(self, board) :
        # estimate future cost by sum of tile displacements
        future = 0
        for sq in range(self.dim*self.dim):
            array = board.split('#')
            occupant = array[sq]
            if occupant != '_' :
                # print("Occupant: ", occupant)
                # print("Goal : ", self.goal)
                shouldbe = findGoal(self.goal,occupant)
                # print("Shouldbe : ",shouldbe)
                future  += self.manTable[(sq,shouldbe)]
        return future
    
    def makeManhatten(self) :
        self.manTable = {}; Dim = self.dim
        for aa in range(Dim*Dim) :
            for bb in range(Dim*Dim) :
                arow = aa//Dim; acol=aa%Dim
                brow = bb//Dim; bcol=bb%Dim
                self.manTable[(aa,bb)] = abs(arow-brow)+abs(acol-bcol)

    def printBoard(self, board, mesg="", sep="\f") :
        if sep  : print(sep)
        if mesg : print(mesg)
        expand = ["%02s"%x for x in board]
        rows = [0]*self.dim
        for i in range(self.dim) :
            rows[i] = "".join(expand[self.dim*i:self.dim*(i+1)])
        print("\n".join(rows))

def scream(error) :
    sys.stderr.write("Error: %s\n" % error)
    sys.stdout.write("Error: %s\n" % error)
    sys.exit(1)

legalMoves3 = ( # for a 3x3 board
   (1,3     ),  # these can slide into square 0
   (0,4,2),     # these can slide into square 1
   (1,5),       # these can slide into square 2
   (0,4,6),     # these can slide into square 3
   (1,3,5,7),   # these can slide into square 4
   (2,4,8),     # these can slide into square 5
   (3,7),       # these can slide into square 6
   (4,6,8),     # these can slide into square 7
   (5,7))       # these can slide into square 8

legalMoves4 = ( # for a 4x4 board
   (1,4     ),  # these can slide into square  0
   (0,5,2),     # these can slide into square  1
   (1,6,7),     # these can slide into square  2
   (2,7),       # these can slide into square  3
   (0,5,8),     # these can slide into square  4
   (1,4,6,9),   # these can slide into square  5
   (2,5,7,10),  # these can slide into square  6
   (3,6,11),    # these can slide into square  7
   (4,9,12),    # these can slide into square  8
   (5,8,10,13), # these can slide into square  9
   (6,9,11,14), # these can slide into square 10
   (7,10,15),   # these can slide into square 11
   (8,13),      # these can slide into square 12
   (9,12,14),   # these can slide into square 13
   (10,13,15),  # these can slide into square 14
   (11,14))     # these can slide into square 15

def legalString(rowCount):
    if rowCount is 3:
        return ((1,3),(0,4,2),(1,5),(0,4,6),(1,3,5,7),(2,4,8),(3,7),(4,6,8),(5,7))

    elif rowCount is 4:
        return ((1,4),(0,5,2),(1,6,7),(2,7),(0,5,8),(1,4,6,9),(2,5,7,10),(3,6,11),(4,9,12),(5,8,10,13),(6,9,11,14),(7,10,15),(8,13),(9,12,14),(10,13,15),(11,14))

    elif rowCount is 2:
        return ((1,2),(0,3),(0,3),(1,2))

def goalExpr(rowCount):
    expr = ""

    for i in range(1,rowCount*rowCount):
        expr += str(i) + "#"
    expr += "_"

    return expr

def findGoal(goal,occupant):
    array = goal.split('#')
    # print("Splitted Goal: ", array)
    for itr in range(len(array)):
        # print("Element: ", array[itr])
        if array[itr] == occupant:
            return itr
    return -1

def findEmpty(array):

    for itr in range(len(array)):
        if array[itr] == '_':
            return itr
    
    return -1