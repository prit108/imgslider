import random

logarr = []

class IDAStar:
    def __init__(self, h, neighbours):
        """ Iterative-deepening A* search.

        h(n) is the heuristic that gives the cost between node n and the goal node. It must be admissable, meaning that h(n) MUST NEVER OVERSTIMATE the true cost. Underestimating is fine.

        neighbours(n) is an iterable giving a pair (cost, node, descr) for each node neighbouring n
        IN ASCENDING ORDER OF COST. descr is not used in the computation but can be used to
        efficiently store information about the path edges (e.g. up/left/right/down for grids).
        """

        self.h = h
        self.neighbours = neighbours
        self.FOUND = object()


    def solve(self, root, is_goal, max_cost=None, file=None):
        """ Returns the shortest path between the root and a given goal, as well as the total cost.
        If the cost exceeds a given max_cost, the function returns None. If you do not give a
        maximum cost the solver will never return for unsolvable instances."""
        global logarr
        self.is_goal = is_goal
        self.path = [root]
        self.is_in_path = {root}
        self.path_descrs = []
        self.nodes_evaluated = 0

        bound = self.h(root)

        logarr.append(stringify(list(root)))
        file.write(stringify(list(root)) + "\n")

        while True:
            t = self._search(0, bound, file)
            if t is self.FOUND: return self.path, self.path_descrs, bound, self.nodes_evaluated
            if t is None: return None
            bound = t

    def _search(self, g, bound, logfile):
        global logarr
        self.nodes_evaluated += 1
    
        node = self.path[-1]
        f = g + self.h(node)


        if f > bound: return f
        if self.is_goal(node): return self.FOUND

        m = None # Lower bound on cost.
        for cost, n, descr in self.neighbours(node):
            if n in self.is_in_path: 
                #logfile.write(stringify(list(n)) + "\n")
                #logarr.append(stringify(list(n)))
                continue

            if(len(logarr) == 0 or logarr[len(logarr) -1] != stringify(list(n))) : 
                logfile.write(stringify(list(n)) + "\n")
                logarr.append(stringify(list(n)))

            self.path.append(n)
            self.is_in_path.add(n)
            self.path_descrs.append(descr)
            t = self._search(g + cost, bound, logfile)

            if t == self.FOUND: return self.FOUND
            if m is None or (t is not None and t < m): m = t

            if(len(logarr) == 0 or logarr[len(logarr) -1] != stringify(list(n))) : 
                logfile.write(stringify(list(n)) + "\n")
                logarr.append(stringify(list(n)))
            logfile.write(stringify(list(node)) + "\n")
            logarr.append(stringify(list(node)))      

            self.path.pop()
            self.path_descrs.pop()
            self.is_in_path.remove(n)

        return m


def slide_solved_state(n):
    return tuple(i % (n*n) for i in range(1, n*n+1))

def slide_randomize(p, neighbours):
    for _ in range(len(p) ** 2):
        _, p, _ = random.choice(list(neighbours(p)))
    return p

def slide_neighbours(n):
    movelist = []
    for gap in range(n*n):
        x, y = gap % n, gap // n
        moves = []
        if x > 0: moves.append(-1)    # Move the gap left.
        if x < n-1: moves.append(+1)  # Move the gap right.
        if y > 0: moves.append(-n)    # Move the gap up.
        if y < n-1: moves.append(+n)  # Move the gap down.
        movelist.append(moves)

    def neighbours(p):
        gap = p.index(0)
        l = list(p)

        for m in movelist[gap]:
            l[gap] = l[gap + m]
            l[gap + m] = 0
            yield (1, tuple(l), (l[gap], m))
            l[gap + m] = l[gap]
            l[gap] = 0

    return neighbours

def slide_print(p):
    n = int(round(len(p) ** 0.5))
    l = len(str(n*n))
    for i in range(0, len(p), n):
        print(" ".join("{:>{}}".format(x, l) for x in p[i:i+n]))

def encode_cfg(cfg, n):
    r = 0
    b = n.bit_length()
    for i in range(len(cfg)):
        r |= cfg[i] << (b*i)
    return r


def gen_wd_table(n):
    goal = [[0] * i + [n] + [0] * (n - 1 - i) for i in range(n)]
    goal[-1][-1] = n - 1
    goal = tuple(sum(goal, []))

    table = {}
    to_visit = [(goal, 0, n-1)]
    while to_visit:
        cfg, cost, e = to_visit.pop(0)
        enccfg = encode_cfg(cfg, n)
        if enccfg in table: continue
        table[enccfg] = cost

        for d in [-1, 1]:
            if 0 <= e + d < n:
                for c in range(n):
                    if cfg[n*(e+d) + c] > 0:
                        ncfg = list(cfg)
                        ncfg[n*(e+d) + c] -= 1
                        ncfg[n*e + c] += 1
                        to_visit.append((tuple(ncfg), cost + 1, e+d))

    return table

def slide_wd(n, goal):
    wd = gen_wd_table(n)
    goals = {i : goal.index(i) for i in goal}
    b = n.bit_length()

    def h(p):
        ht = 0 # Walking distance between rows.
        vt = 0 # Walking distance between columns.
        d = 0
        for i, c in enumerate(p):
            if c == 0: continue
            g = goals[c]
            xi, yi = i % n, i // n
            xg, yg = g % n, g // n
            ht += 1 << (b*(n*yi+yg))
            vt += 1 << (b*(n*xi+xg))

            if yg == yi:
                for k in range(i + 1, i - i%n + n): # Until end of row.
                    if p[k] and goals[p[k]] // n == yi and goals[p[k]] < g:
                        d += 2

            if xg == xi:
                for k in range(i + n, n * n, n): # Until end of column.
                    if p[k] and goals[p[k]] % n == xi and goals[p[k]] < g:
                        d += 2

        d += wd[ht] + wd[vt]

        return d
    return h


def stringify(board):

    temp = ""
    for itr in range(0,len(board)):
        if board[itr] is 0:
            temp += "_#"
        else:
            temp += str(board[itr]) + "#"

    temp = temp[0:len(temp)-1]

    return temp


def finalArray(moves,board):

    arr = []

    board = list(board)
    itr1 = 0
    itr2 = 0

    for itr in range(0,len(board)):
        if board[itr] is 0:
            itr1 = itr

    temp = board
    count = 0
    arr.append(stringify(temp))

    while count < len(moves):
        for itr in range(0, len(temp)):
            if temp[itr] is moves[count][0]:
                itr2 = itr
        
        temp[itr1], temp[itr2] = temp[itr2], temp[itr1]
        itr1 = itr2
        arr.append(stringify(temp))
        count = count + 1

    print("Array")
    print(arr)

    return arr



def play(board, dimension, file):
    global logarr
    logarr = []
    solved_state = slide_solved_state(dimension)
    neighbours = slide_neighbours(dimension)
    is_goal = lambda p: p == solved_state

    slide_solver = IDAStar(slide_wd(dimension, solved_state), neighbours)

    path, moves, cost, num_eval = slide_solver.solve(board, is_goal, 1000, file)

    return finalArray(moves,board), logarr

if __name__ == "__main__":

    solved_state = slide_solved_state(4)
    neighbours = slide_neighbours(4)
    is_goal = lambda p: p == solved_state

    # tests = [
        #(5,1,7,3,9,2,11,4,13,6,15,8,0,10,14,12),
        #(2,5,13,12,1,0,3,15,9,7,14,6,10,11,8,4),
        #(5,2,4,8,10,0,3,14,13,6,11,12,1,15,9,7),
        #(11,4,12,2,5,10,3,15,14,1,6,7,0,9,8,13),
        #(5,8,7,11,1,6,12,2,9,0,13,10,14,3,4,15),
        #(5,7,2,3,1,6,9,11,4,12,8,14,0,13,10,15),
        # (1,2,0,4,7,15,3,8,5,9,10,11,13,12,14,6)
    # ]

    slide_solver = IDAStar(slide_wd(4, solved_state), neighbours)

    for p in tests:
        path, moves, cost, num_eval = slide_solver.solve(p, is_goal, 1000)
        slide_print(p)
        print(", ".join({-1: "Left", 1: "Right", -4: "Up", 4: "Down"}[move[1]] for move in moves))
        print(cost, num_eval)