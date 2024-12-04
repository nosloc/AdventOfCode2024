import sys 
from enum import Enum

class Direction(Enum):
    Right = (0,1)
    Left = (0,-1)
    Down = (1, 0)
    Up = (-1,0)
    DownLeft = (Left[0]+Down[0], Left[1]+Down[1])
    DownRight = (Right[0]+Down[0], Right[1]+Down[1])
    UpLeft = (Left[0]+Up[0], Left[1]+Up[1])
    UpRight = (Right[0]+Up[0], Right[1]+Up[1])

allDirections = [d for d in Direction]
diagonals = [Direction.UpLeft, Direction.UpRight, Direction.DownLeft, Direction.DownRight]

def parse(inputFileName):
    with open(inputFileName) as file:
        lines = file.readlines()
        lines = list(map(lambda s: s.replace("\n", ""), lines))
        height = len(lines[0])
        width = len(lines)
        return lines, height, width

def isInbound(height, width, i, j):
    return i >= 0 and i < height and j >= 0 and j < width

def verif(lines, height, width, i, j, direction, expectedString):
    # Right
    for l in range(len(expectedString)):
        x = i+direction.value[0]*l
        y = j+direction.value[1]*l
        if not isInbound(height, width, x, y):
            return False
        if not lines[x][y]== expectedString[l]:
            return False
    return True

def solve(lines, height, width, expectedString, checkingDirections, Xshape):
    xmasCounter = 0
    for i in range(height):
        for j in range(width):
            if lines[i][j]==expectedString[0]:
                for d in checkingDirections:
                    if verif(lines, height, width, i, j, d, expectedString):
                        if Xshape:
                            spaceBetween = len(expectedString) - 1
                            x1, y1 = i, j + d.value[1]*spaceBetween
                            d1 = Direction(d.value[0], -d.value[1])
                            if verif(lines, height, width, x1, y1, d1, expectedString):
                                xmasCounter += 1
                            x2, y2 = i + d.value[0]*spaceBetween, j
                            d2 = Direction(-d.value[0], d.value[1])
                            if verif(lines, height, width, x2, y2, d2, expectedString):
                                xmasCounter += 1
                        else :
                            xmasCounter += 1
    return xmasCounter if not Xshape else int(xmasCounter/2)

    
# Main

inputFileName = "input.txt"
if len(sys.argv) > 1 and sys.argv[1] == "-t":
    inputFileName = "test.txt"
lines, height, width = parse(inputFileName)
if lines == None:
    print(f"An issue occured when trying to read the file {inputFileName}")
answer1 = solve(lines, height, width, "XMAS", allDirections, False)
print(f"Answer1: {answer1}")
answer2 = solve(lines, height, width, "MAS", diagonals, True)
print(f"Answer2: {answer2}")