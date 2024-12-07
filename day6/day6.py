import sys
from enum import Enum

class Direction:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __repr__(self):
        return f"Direction({self.x}, {self.y})"

Up = Direction(0, 1)
Down = Direction(0, -1)
Left = Direction(-1, 0)
Right = Direction(1, 0)

def rotate(direction):
    if direction == Up:
        return Right
    elif direction == Right:
        return Down
    elif direction == Down:
        return Left
    elif direction == Left:
        return Up

class CellStates(Enum):
    Empty = "."
    Chair = "#"
    Visited = "X"
    CreatedObstacle = "O"

class MapCell:
    def __init__(self, state):
        self.state = state
        self.directions = set()
    
    def __repr__(self):
        return self.state.value
    
    def show(self):
        print(f"MapCell({self.state.value} {self.directions})")

class Map:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.cells = [[MapCell(CellStates.Empty) for i in range(height)] for j in range(width)]
    def get(self, x,y):
        return self.cells[x][y] 
    def __repr__(self):
        result = ""
        for i in range(self.height-1, -1, -1):
            for j in range(self.width):
                result  += str(self.cells[j][i])
            result += "\n"
        return result
    def inBounds(self, x, y):
        return x >= 0 and x < self.width and y >= 0 and y < self.height
    def copy(self):
        m2 = Map(self.height, self.width)
        for i in range(self.width):
            for j in range(self.height):
                m2.cells[i][j].state = self.cells[i][j].state
                m2.cells[i][j].directions = self.cells[i][j].directions.copy()
        return m2
        

def parse(fileName):
    with open(fileName) as file:
        lines = file.readlines()
        return list(map(lambda e: e.replace("\n", ""), lines))
    
def formatInput(lines):
    height = len(lines)
    width = len(lines[0])
    m = Map(height, width)
    initialPosition = (-1, -1)
    for i in range(m.height):
        for j in range(m.width):
            x = j
            y = height - i - 1
            c = lines[i][j]
            if (c == "^"):
                initialPosition = (x, y)
                c = "."
            m.get(x,y).state = CellStates(c)
    return m, initialPosition

def moveStraight(x, y, direction, m):
    nextX = x + direction.x
    nextY = y + direction.y
    if not m.inBounds(nextX, nextY):
        return nextX, nextY
    if m.get(nextX, nextY).state == CellStates.Chair or m.get(nextX, nextY).state == CellStates.CreatedObstacle:
        return x, y
    else:
        return moveStraight(nextX, nextY, direction, m)

def visitCell(m, x, y, d, counterVisited):
    if m.inBounds(x, y):
        cell = m.get(x, y)
        cell.directions.add(d)
        if cell.state != CellStates.Visited:
            counterVisited += 1
            cell.state = CellStates.Visited
        #print(m)
        #print("===================================")
    x += d.x
    y += d.y
    return x, y, counterVisited

def traverseAndCount(m, initialPosition, direction, verifyLoops = False):
    x, y = initialPosition
    d = direction
    counterVisited = 0
    counterAll = 0
    first = True
    while m.inBounds(x, y):
        nextX, nextY = moveStraight(x, y, d, m)
        if m.inBounds(x, y) and d in m.get(x,y).directions and verifyLoops and not first:
            return True
        first = False
        while x != nextX or y != nextY:
            if verifyLoops:
                if m.inBounds(x, y) and d in m.get(x,y).directions:
                    return True
            x, y, counterVisited = visitCell(m, x, y, d, counterVisited)
            counterAll += 1
        _, _, counterVisited = visitCell(m, x, y, d, counterVisited)
        counterAll += 1
        d = rotate(d)
    #print()
    if verifyLoops:
        return False
    return counterVisited, counterAll

def veirfyLoops(m, position, direction, initialPosition, tested):
    x, y = position
    oX, oY = (x+direction.x, y+direction.y)
    m1 = m.copy()
    #print(f"Checking loops at {x}, {y} with direction {direction}")
    #print(f"Obstacle at {oX}, {oY}")
    if (m1.inBounds(oX, oY) and m1.get(oX, oY).state != CellStates.Chair and (oX, oY) != initialPosition and (oX, oY) not in tested):
        m1.get(oX, oY).state = CellStates.CreatedObstacle
        res = traverseAndCount(m1, (x, y), direction, True)
        #print(f"Result: {res}\n")
        tested.append((oX, oY))
        return res
    #print("Obstacle or out of bounds\n")
    return False

def CountPossibleLoops(m, initialPosition, direction,length):
    x, y = initialPosition
    d = direction
    counterloops = 0
    tested = []
    i = 0
    while m.inBounds(x, y):
        nextX, nextY = moveStraight(x, y, d, m)
        while x != nextX or y != nextY:
            print(f"Progress: {i/length*100:.2f}%", end="\r")
            visitCell(m, x, y, d, 0)
            if veirfyLoops(m, (x, y), d, initialPosition, tested):
                counterloops += 1
            x, y = x + d.x, y + d.y
            i += 1
        visitCell(m, x, y, d, 0)
        i+=1
        print(f"Progress: {i/length*100:.2f}%", end="\r")
        d = rotate(d)
    print()
    return counterloops

def solve1(lines):
    m, initialPosition = formatInput(lines)
    return traverseAndCount(m, initialPosition, Up)


def solve2(lines, length=1):
    m, initialPosition = formatInput(lines)
    return CountPossibleLoops(m, initialPosition, Up, length)



# Main 
if __name__ == "__main__":
    fileName = "input.txt"
    if len(sys.argv) >=2 and sys.argv[1] == "-t":
        fileName="test.txt"
    lines = parse(fileName)
    answer1 = solve1(lines)
    print(f"Answer1: {answer1[0]}")
    print(f"Length: {answer1[1]}")
    answer2 = solve2(lines, answer1[1])
    print(f"Answer1: {answer2}")
