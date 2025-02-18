import sys
from enum import Enum

class Tile(Enum):
    Empty = "."
    Corrupted = "#"
    Path = "O"

Up = (-1, 0)
Down = (1, 0)
Right = (0, 1)
Left = (0, -1)

all_directions = [Up, Down, Right, Left]

class Node():
    def __init__(self):
        self.type = Tile.Empty
        self.pred = None
    def __repr__(self):
        return self.type.value

def parse(inputFile):
    corrupted = []

    with open(inputFile) as file:
        for l in file.readlines():
            x, y = l.replace("\n", "").split(",")
            x = int(x)
            y = int(y)
            corrupted.append((x,y))
    return corrupted

def createMap(height, width):
    m = [[Node() for _ in range(width)] for _ in range(height)]
    return m

def mapAfterCorruption(corrupted, m):
    for x, y in corrupted:
        m[y][x].type = Tile.Corrupted
        
def printMap(m, height, width, path =[], interstingNode = (-1, -1)):
    for y in range(height):
        for x in range(width):
            if (x, y) == interstingNode:
                print("X", end= " ")
                continue
            if len(path) == 0:
                print(m[y][x].type.value, end=" ")
            else :
                if (x, y) in path:
                    print("O", end =" ")
                elif (m[y][x].type == Tile.Corrupted):
                    print(Tile.Corrupted.value, end= " ")
                else :
                    print(".", end=" ")

        print()

def BFS(m, start, end, height, width):
    in_bound = lambda x, y: x >= 0 and x < width and y>=0 and y < height
    nextToVisit = set()
    nextToVisit.add(start)
    step = 0
    while(len(nextToVisit) != 0):
        temp = nextToVisit.copy()
        nextToVisit = set()
        for tile in temp:
            curr_x = tile[0]
            curr_y = tile[1]
            m[curr_y][curr_x].type =  Tile.Path
            #printMap(m, height, width)
            if (curr_x, curr_y) == end:
                return step
            for dx, dy in all_directions:
                next_x = curr_x + dx
                next_y = curr_y + dy
                if (in_bound(next_x, next_y) and m[next_y][next_x].type == Tile.Empty):
                    m[next_y][next_x].pred = (curr_x, curr_y)
                    nextToVisit.add((next_x, next_y))
        step += 1
    return -1

def retreivePath(m, upTo):
    nX, nY = upTo
    end = False
    pred = None
    path = []
    while not end:
        path.append((nX, nY))
        pred = m[nY][nX].pred
        if pred == None:
            end = True
            return path
        nX, nY = pred
    return None




def solve1(corrupted, height, width, test=False):
    if test :
        corrupted = corrupted[:12]
    corrupted = corrupted[:1024]
    m = createMap(height, width)
    mapAfterCorruption(corrupted, m)
    #printMap(m, height, width)
    ret = BFS(m, (0,0), (height -1, width-1), height, width)
    path = retreivePath(m, (height - 1, width - 1))
    #print(path)
    #printMap(m, height, width, path)
    return path, ret
    
def solve2(corrupted, height, width):
    upper = len(corrupted)
    lower = 0
    tested_length = 0
    while lower + 1 < upper:
        tested_length = (lower + upper)//2
        m = createMap(height, width)
        mapAfterCorruption(corrupted[:tested_length], m)
        ret = BFS(m, (0,0), (height-1, width-1), height, width)
        if ret != -1:
            #printMap(m, height, width, retreivePath(m, (height-1, width-1)))
            #print(f"{tested_length} is working with {ret} nodes in the best path")
            lower = tested_length
            #print(lower, upper, tested_length)
        else:
            #print(f"{tested_length} is not working")
            upper = tested_length 
            #print(lower, upper, tested_length)
        #print()

    """
    # Printing the last maps where it has a path and then the one without a path
    m_1 = createMap(height, width)
    mapAfterCorruption(corrupted[:lower], m_1)
    ret = BFS(m_1, (0,0), (height-1, width-1), height, width)
    print(ret)
    printMap(m_1, height, width, retreivePath(m_1, (height -1, width-1)), corrupted[lower-1])
    print()
    m_2 = createMap(height, width)
    mapAfterCorruption(corrupted[:lower + 1], m_2)
    printMap(m_2, height, width, [], corrupted[lower])
    """
    return corrupted[lower]

#Main 

input_file = "input.txt"
width = 71
height = 71
test = False
if  "-t" in sys.argv :
    input_file = "test.txt"
    width = 7
    height = 7
    test = True
corrupted = parse(input_file)
path, answer1 = solve1(corrupted, height, width, test)
print(f"Answer 1: {answer1}")
answer2 = solve2(corrupted, height, width)
print(f"Answer 2: {answer2}")

