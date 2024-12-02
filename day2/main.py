import sys


# Parse function
def parse(inputPath):
    with open(inputPath) as file:
        return file.readlines()
    return None

def format(inputData):
    # Format the input 
    lines = []   
    for s in inputData:
        line = []
        for value in s.split():
            line.append(int(value))
        lines.append(line)
    return lines

def verifyLine(l, tolerent):
    # Lines with a single or none levels
    if len(l) <=1:
        return True
    # Line with multiple levels
    else:
        isIncreasing = True
        if l[0] > l[1]:
            isIncreasing = False
        
        for i in range(1, len(l)):
            diff = l[i]-l[i-1]
            if not isIncreasing:
                diff = -diff 
            if diff < 1 or diff > 3:
                if tolerent:
                    # Whitout value at index i
                    option1 = l[:i] + l[i+1:]
                    # whithout value before i
                    option2 = l[:i-1] + l[i:]
                    # Whitout first value in case ordering was wrong
                    option3 = l[1:]
                    safe = verifyLine(option1, False) or verifyLine(option2, False) or verifyLine(option3, False)
                    return safe
                return False
        return True

def solve(inputData, tolerent):
    lines = format(inputData)
    safeCounter = 0

    # Verify each line
    for l in lines:
            if verifyLine(l, tolerent):
                safeCounter += 1
    return safeCounter


# Puzzle 1
def solve1(inputData):
    return solve(inputData, False)

# Puzzle 2
def solve2(inputData):
    return solve(inputData, True) 


# Main 

inputFileName = "input.txt"
if len(sys.argv) > 1 and sys.argv[1] == "-t":
    inputFileName = "test.txt"
lines = parse(inputFileName)
if lines == None:
    print(f"An issue occured when trying to read the file {inputFileName}")
answer1 = solve1(lines)
print(f"Answer1: {answer1}")
answer2 = solve2(lines)
print(f"Answer2: {answer2}")