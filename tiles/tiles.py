# tiles.py
#
import sys

class TileGame :
    def __init__ (self, sampleBoard) :
        self.legalMoves = legalMoves3
        self.goal       = "12345678_"
        self.dim        = 3   
        self.makeManhatten()

    def getMoves(self, board) :
        empty = board.find('_')
        return empty, self.legalMoves[empty]
    
    def makeMove(self, board, empty, mov) :
        lbrd = list(board)
        lbrd[empty],lbrd[mov] = lbrd[mov],lbrd[empty]
        return "".join(lbrd)
    
    def futureCost(self, board) :
        # estimate future cost by sum of tile displacements
        future = 0
        for sq in range(self.dim*self.dim):
            occupant = board[sq]
            if occupant != '_' :
                shouldbe = self.goal.find(occupant)
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

