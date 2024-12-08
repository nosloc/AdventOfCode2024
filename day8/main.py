import sys

acceptablechars="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

def gcc(x,y):
    while y != 0:
        t = y
        y = x%y
        x = t
    return abs(x)


def parse(inputFileName):
    with open(inputFileName) as file:
        return list(map(lambda s: s.replace("\n", ""), file.readlines()))

def addAntinodes1(c, x, y, previousAntennas, inbound, antinodes):
    others = previousAntennas.get(c, set())
    for x1, y1 in others:
        dx, dy = x - x1, y - y1
        antiX = x + dx 
        antiY = y + dy
        if (inbound(antiX, antiY)):
            antinodes.add((antiX,antiY))
        antiX = x1 - dx
        antiY = y1 - dy
        if (inbound(antiX, antiY)):
            antinodes.add((antiX, antiY))

def addAntinodes2(c, x, y, previousAntennas, inbound, antinodes):
    others = previousAntennas.get(c, set())
    for x1, y1 in others:
        dx, dy = x - x1, y -y1
        div = gcc(dx,dy)
        dx = dx//div
        dy = dy//div
        i = 0
        stop = False
        antiX, antiY = x, y
        while (not stop):
            antiX =  x + i*dx
            antiY = y + i*dy
            if (inbound(antiX, antiY)):
                antinodes.add((antiX,antiY))
                stop = False
            else :
                stop = True
            antiX = x - i*dx
            antiY = y - i*dy
            if (inbound(antiX, antiY)):
                antinodes.add((antiX,antiY))
                stop = False
            else :
                stop = stop and True
            i+=1
            


def solve(lines, method):
    previousAntennas = {}
    antinodes = set()
    height = len(lines)
    width = len(lines[0])
    inbound = lambda x,y: x>=0 and x<height and y>=0 and y<width
    for x in range(height):
        for y in range(width):
            c = lines[x][y]
            if c in acceptablechars:
                method(c, x, y, previousAntennas, inbound, antinodes)
                s = previousAntennas.get(c, set())
                s.add((x,y))
                previousAntennas[c] = s
    return len(antinodes)
    

# Main
inputFile = "input.txt"
if len(sys.argv)> 1 and sys.argv[1] == '-t':
    inputFile = "test.txt"
lines = parse(inputFile)
answer1 = solve(lines, addAntinodes1)
print(f"Answer1 : {answer1}")
answer2 = solve(lines, addAntinodes2)
print(f"Answer2 : {answer2}")