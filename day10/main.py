import sys


directions = [(0,1), (0,-1), (1,0), (-1,0)]
class Position():
    def __init__(self,x,y):
        self.x = x
        self.y = y
    def __hash__(self):
        return hash((self.x,self.y))
    def __repr__(self):
        return f"Pos{self.x, self.y}"
    def __eq__(self, value):
        value.x == self.x and value.y == self.y
    def toTuple(self):
        return (self.x, self.y)

class Node():
    def __init__(self, p, value):
        self.position = p
        self.nexts = set()
        self.value = value
    
    def __repr__(self):
        return f"Node({self.position},{self.value}, nexts={[n.position for n in self.nexts]})"



def debugPrint(s):
    if (debug):
        print(f"Debug : {s}")

def printGraph(g, prefix=""):
    debugPrint(f"{prefix}-({g.position},{g.value})")
    if (len(g.nexts)!=0):
        for g1 in g.nexts:
            printGraph(g1, prefix=prefix+"\t")

def findAllFinalNode(g):
    if (g.value==9):
        s = set()
        s.add(g.position.toTuple())
        return s
    if (len(g.nexts)==0):
        return set()
    finalNodes=set()
    for head in g.nexts:
        for elem in (findAllFinalNode(head)):
            finalNodes.add(elem)
    return finalNodes
    
def countNumberOfTrails(g):
    if (g.value==9):
        return 1
    if (len(g.nexts)==0):
        return 0
    ratings = map(lambda head: countNumberOfTrails(head), g.nexts)
    return sum(ratings)

def parse(input):
    table = []
    with open(input) as file:
        for l in file.readlines():
            l = l.replace("\n", "")
            table.append(list(map(lambda c: int(c), l)))
        return table

def formatInput(t):
    width = len(t[0])
    height = len(t)
    zeroes = set()
    table = {}
    inBound = lambda pos: pos.x < height and pos.x >= 0 and pos.y < width and pos.y >= 0
    for i in range(len(t)):
        inputLine = t[i]
        for j in range(len(inputLine)):
            currentPosition = Position(i,j)
            currentValue = inputLine[j]
            currentNode = table.get(currentPosition.toTuple(), Node(currentPosition, currentValue))
            if (currentValue == 0):
                zeroes.add(currentNode)
            for dx, dy in directions:
                checkingPos = Position(currentPosition.x + dx, currentPosition.y + dy)
                if (inBound(checkingPos)):
                    checkingnode = table.get(checkingPos.toTuple(), Node(checkingPos, t[checkingPos.x][checkingPos.y]))
                    if (currentNode.value == checkingnode.value -1):
                        currentNode.nexts.add(checkingnode)
                    table[checkingPos.toTuple()]= checkingnode
            table[currentPosition.toTuple()] = currentNode
    return zeroes

def solve(tableInput, rating=False):
    zeroes = formatInput(tableInput)
    counter = 0
    for z in zeroes:
        if (not rating):
            s = findAllFinalNode(z)
            debugPrint(f"for {z} all finalNodes are {s}")
            counter += len(s)
        else:
            counter += countNumberOfTrails(z)
    return counter






# Main 
inputFile = "input.txt"
args = sys.argv
debug = False
if "-t" in args:
    inputFile = "test.txt"
if "-d" in args:
    debug = True

if debug:
    print("Debugging :")

table = parse(inputFile)
answer1 =solve(table)
print("Answer1: ", answer1)
answer2 = solve(table, True)
print(f"Answer2 : {answer2}")