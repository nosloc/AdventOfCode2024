import sys
import math
import heapq

class DjikstraNode():
    def __init__(self, x, y, direction,cost, neighbors, edgeCosts):
        self.x = x
        self.y = y
        self.cost = cost
        self.neighbors = neighbors
        self.edgeCosts = edgeCosts
        self.direction = direction
    def __repr__(self):
        return f"DjikstraNode({self.x, self.y}, {self.cost},{self.direction})"
    def __lt__(self, other):
        return self.cost < other.cost
    def addNeighbor(self, neighbor, edgeCost):
        if neighbor in self.neighbors:
            return
        self.neighbors.append(neighbor)
        self.edgeCosts.append(edgeCost)
        #neighbor.neighbors.append(self)
        #neighbor.edgeCosts.append(edgeCost)
    def __hash__(self):
        return hash((self.x, self.y, self.direction))
    
    

class Node():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.north = DjikstraNode(x, y, North, math.inf, [], [])
        self.south = DjikstraNode(x, y, South, math.inf, [], [])
        self.east = DjikstraNode(x, y, East, math.inf, [], [])
        self.west = DjikstraNode(x, y, West, math.inf, [], [])
        self.north.addNeighbor(self.east, 1000)
        self.north.addNeighbor(self.west, 1000)
        self.south.addNeighbor(self.east, 1000)
        self.south.addNeighbor(self.west, 1000)
        self.east.addNeighbor(self.north, 1000)
        self.east.addNeighbor(self.south, 1000)
        self.west.addNeighbor(self.north, 1000)
        self.west.addNeighbor(self.south, 1000)
    def addNeighbor(self, neighbor, edgeCost, direction):
        if direction == North:
            self.north.addNeighbor(neighbor.north, edgeCost)
        elif direction == South:
            self.south.addNeighbor(neighbor.south, edgeCost)
        elif direction == East:
            self.east.addNeighbor(neighbor.east, edgeCost)
        elif direction == West:
            self.west.addNeighbor(neighbor.west, edgeCost)
    def __repr__(self):
        return f"Node({self.x, self.y}, north: {self.north}, south: {self.south}, east: {self.east}, west: {self.west})"

North = (-1, 0)
South = (1, 0)
East = (0, 1)
West = (0, -1)
directions = [North, South, East, West]

def parse(inputFileName):
    lines = []
    with open(inputFileName) as file:
        lines = [list(s.replace("\n", "")) for s in file.readlines()]
    return lines

def createGraph(lines):
    height = len(lines)
    width = len(lines[0])
    start = None
    end = None
    mazeMap = [[None for _ in range(width)] for _ in range(height)]
    nodes = set()
    for x in range(height):
        for y in range(width):
            if (lines[x][y] != "#"):
                node = Node(x, y)
                mazeMap[x][y] = node
                nodes.add(node)
            if lines[x][y] == "S":
                start = node
            if lines[x][y] == "E":
                end = node
    for x in range(1, height-1):
        for y in range(1, width-1):
            if mazeMap[x][y] == None:
                continue
            for dx, dy in directions:
                if (mazeMap[x+dx][y+dy] != None):
                    mazeMap[x][y].addNeighbor(mazeMap[x+dx][y+dy], 1, (dx, dy))
    return start, end, nodes

def dijkstra(start, end, nodes):
    # For each node keep 4 booleans North, South, East, West that are visited or not
    visited = set()
    start.east.cost = 0
    hq = [start.east]
    heapq.heapify(hq)
    predecessors = {}
    while len(visited) < len(nodes)*4:
        current = heapq.heappop(hq)
        if current in visited:
            continue
        visited.add(current)
        for i in range(len(current.neighbors)):
            neighbor = current.neighbors[i]
            edgeCost = current.edgeCosts[i] 
            newCost = current.cost + edgeCost
            if newCost < neighbor.cost:
                predecessors[neighbor] =  [current]
                neighbor.cost = newCost
                heapq.heappush(hq, neighbor)
            elif newCost == neighbor.cost:
                predecessors[neighbor] = predecessors.get(neighbor, set()) + [current]
    return predecessors


def solve(inputNameFile):
    start, end, nodes = createGraph(parse(inputNameFile))
    predecessors = dijkstra(start, end, nodes)
    answer1 = min([end.north.cost, end.south.cost, end.east.cost, end.west.cost])
    ends = [n for n in [end.north, end.south, end.east, end.west] if n.cost == answer1]
    on_path = retreiveNodesOnPath(ends, predecessors)
    big_nodes_on_path = set([(n.x,n.y) for n in on_path])
    answer2 = len(big_nodes_on_path)

    return answer1, answer2

def retreiveNodesOnPath(ends, predecessors):
    on_path = set(ends)
    nexts = ends
    while(len(nexts) > 0):
        curr = nexts.pop()
        for elem in predecessors.get(curr,[]):
            nexts.append(elem)
            on_path.add(elem)
    return on_path
        


inputFile = "input.txt"
if "-t" in sys.argv:
    inputFile = "test.txt"
answer1, answer2 = solve(inputFile)
print(f"Answer 1: {answer1}")
print(f"Answer 2: {answer2}")