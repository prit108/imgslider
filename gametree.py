from os import setgroups
from queue import Queue
import pygame
import time
#from tkinter import Tk, Canvas, Frame, BOTH

pygame.init()
dimX = 1500
dimY = 1500
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
size = 3
ss = 5
sc = 300
frame = pygame.display.set_mode((dimX,dimY))
pygame.display.update()
clock = pygame.time.Clock()
GOAL_CONFIG = [i for i in range(1,size*size)]
GOAL_CONFIG.append(0)
GOAL_CONFIG = tuple(GOAL_CONFIG)
pygame.display.set_caption("GameTree")

frame.fill((0,0,0))

sol_array = []

def GetSolArray(filename):
    global sol_array
    file = open(filename, "r")
    while True:
        line = file.readline()
        if not line : break
        newline = line.strip("\n")
        array = newline.split('#')
        config = ()
        for x in array :
            if x == '_' :
                config = config + (0,)
            else :
                config = config + (int(x),) 
        sol_array.append(config)
        #print(config)
    file.close()
    return sol_array

def GetSolSet(array) :
    setofconfig = set(array)
    return setofconfig

def GetGapLocation(config) :
    return config.index(0)

def GetNextConfigs(config) :
    global size
    gap = GetGapLocation(config)
    
    x = int(gap//size)
    y = int(gap%size)
    neighbours = []
    
    newconfig = list(config)
    if(x > 0):
        newconfig[x*size + y], newconfig[(x-1)*size + y] = newconfig[(x-1)*size + y], newconfig[x*size + y]
        neighbours.append(tuple(newconfig))
    
    newconfig = list(config)
    if(x < size-1):
        newconfig[x*size + y], newconfig[(x+1)*size + y] = newconfig[(x+1)*size + y], newconfig[x*size + y]
        neighbours.append(tuple(newconfig))
    
    newconfig = list(config)
    if(y > 0):
        newconfig[x*size + y], newconfig[x*size + y-1] = newconfig[x*size + y-1], newconfig[x*size + y]
        neighbours.append(tuple(newconfig))

    newconfig = list(config)
    if(y < size-1):
        newconfig[x*size + y], newconfig[x*size + y+1] = newconfig[x*size + y+1], newconfig[x*size + y]
        neighbours.append(tuple(newconfig))

    return neighbours

class Node :
    def __init__(self, config, parent) :
        global sol_array
        self.config = config
        self.parent = parent
        self.parentnode = None
        self.children = []
        self.childconfig = []
        self.GetChildren()
        self.location = [-1,-1]
        self.circle = None
        #self.children = []

    def copy_constructor(self, orig):
        global sol_array
        self.config = orig.config
        self.parent = orig.parent
        self.children = orig.children
        self.childconfig = orig.childconfig
        self.location = orig.location
    
    def __eq__(self, other):
        return self.config == other.config
        
    def SetParent(self, parent) :
        self.parent = parent
    
    def GetChildren(self) :
        allchild = GetNextConfigs(self.config)
        #allchildnode = []
        if(self.parent is not None):
            allchild.remove(self.parent)
        self.childconfig = allchild
        return

    def CreateChildrenNode(self):
        for x in self.childconfig :
            self.children.append(Node(x,self.config))
         
radii = 5 #radius of node circle
offset = 50 #difference between levels
l_t = 1 #edge line thickness 
mindotdist = dimY//8

def custom_sort(e):
    return e[0]


class GameTree:
    def __init__(self):
        global sol_array
        self.node_array = []
        self.depth = []
        self.data_array = []
        self.root = Node(sol_array[0], None)
        #pygame.draw.circle(frame,white,(dimX/2, offset),radii,0)
        #self.show(self.root, int(dimX/2),(dimX/2, offset))
        self.bfs()
        self.plot()

    def bfs(self):
        q = Queue(maxsize=4*len(sol_array))
        q.put_nowait((self.root,0))
        self.node_array.append(self.root)
        self.depth.append(0)
        #self.data_array.append((0,self.root))
        visited = []
        while(not q.empty()) :
            l = q.get_nowait()
            p = l[0]
            print(p.config)
            d = int(l[1])
            if(p not in visited) :
                d = int(l[1])
                for x in p.childconfig :
                    if x in sol_array :
                        a = Node(x, p.config)
                        p.children.append(a)
                        q.put_nowait((a,d+1))
                        self.node_array.append(a)
                        self.depth.append(d+1)
                        #self.data_array.append((d+1,a))
                visited.append(p)
        
        #self.data_array.sort(key=custom_sort)
        #self.node_array = self.data_array[1]
        #self.depth = self.data_array[0]
        
    
    def plot(self) :
        global offset, dimX
        i:int = 0
        print(len(self.node_array), len(self.depth))
        while(i < (len(self.node_array))) :
            self.node_array[i].location[1] = (self.depth[i] + 1)*offset
            j:int = 0
            while(i+j < len(self.depth) and self.depth[i] == self.depth[i+j]) : j+=1
            dist:int = dimX//(j+1)
            d:int = dist
            k:int = 0
            while(k < j) :
                self.node_array[i+k].location[0] = d
                self.node_array[i+k].location[1] = (self.depth[i] + 1)*offset
                d+=dist
                k+=1
            i+=j

        self.show()


    def show(self) : #, parent:Node, allowed_length , parent_center: tuple):
        #n = len(parent.children)
        #distance = 0
        #if n > 1 :
        #    distance = max(int(allowed_length/(n-1)), mindotdist)
        #if n <= 1 :
        #    start = parent_center[0]
        #else :
        #    start = parent_center[0] - int(allowed_length/2)
        #height = parent_center[1] + offset
        #for i in range(len(parent.children)) :
        #    pygame.draw.circle(frame,white,(start, height),radii,0)
        #    pygame.draw.line(frame,white,parent_center,(start, height),l_t)
        #    self.show(parent.children[i], int(distance/2)-8,(start, height))
        #    start = start + distance
        #return
        #for x in self.node_array:
        #    color = white
        #    if(x.config == GOAL_CONFIG): color = red
        #    elif(x.config == sol_array[0]): color = green
        #    pygame.draw.circle(frame,color,(x.location[0],x.location[1]),radii,0)
        #    pygame.display.update()
        #    for y in x.children: 
        #        pygame.draw.line(frame,white,(x.location[0],x.location[1]),(y.location[0],y.location[1]),l_t)
        #        pygame.display.update()
        #    clock.tick(ss)

        dic_config = {}
        for x in self.node_array:
            dic_config[x.config] = x

        showthese = []

        for c in sol_array :
            color = white
            if(c == GOAL_CONFIG): color = red
            elif(c == sol_array[0]): color = green
            x = dic_config[c]
            if len(showthese) > 1 and showthese[len(showthese)-1].parent == x.config :
                showthese.pop()
            else :
                showthese.append(x)
            for p in self.node_array:
                color = white
                if(p.config == GOAL_CONFIG): color = red
                elif(p.config == sol_array[0]): color = green
                pygame.draw.circle(frame,color,(p.location[0],p.location[1]),radii,0)
                pygame.display.update()
                for y in p.children: 
                    pygame.draw.line(frame,white,(p.location[0],p.location[1]),(y.location[0],y.location[1]),l_t)
                    pygame.display.update()
            
            for y in showthese : 
                color = (255,0,0)
                pygame.draw.circle(frame,color,(y.location[0],y.location[1]),radii,0)
                pygame.display.update()
                for z in y.children :
                    if z in showthese :
                        pygame.draw.line(frame,color,(y.location[0],y.location[1]),(z.location[0],z.location[1]),l_t)
                        pygame.display.update()
                clock.tick(sc)
            
            pygame.draw.circle(frame,color,(x.location[0],x.location[1]),radii,0)
            pygame.display.update()
            clock.tick(ss)
        
        return




if __name__ == '__main__' :
    GetSolArray("./test.txt")
    print(sol_array[0])
    x = GameTree()
    while True:
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                pygame.quit()
                quit()
            pygame.display.update()
