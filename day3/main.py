import sys
import re

def parse(inputPath):
    with open(inputPath) as file:
        return file.read()

# Puzzle 1
def solve1(inputData):
    # Regex for matching substring of this type: "mul(1,223)"
    pattern = r"mul\((\d{1,3}),(\d{1,3})\)"
    mulResults = map(
        lambda c:
            int(c.group(1)) * int(c.group(2)),
        re.finditer(pattern, inputData)
    )
    return sum(mulResults)

# Puzzle 2
def solve2(inputData):
    # Match mul(x,y), do(), don't()
    pattern = r"mul\(\d{1,3},\d{1,3}\)|do\(\)|don\'t\(\)"
    commands = re.findall(pattern, inputData)
    #print(commands)
    isenable = True
    totalSum = 0
    for c in commands:
        match c:
            case "do()":
                isenable = True
            case "don't()":
                isenable = False
            case _:
                if isenable:
                    a,b = re.findall(r"\d{1,3}",c)
                    a = int(a)
                    b = int(b)
                    totalSum += a * b
    return totalSum


# Main 


data1 = ""
data2 = ""
if len(sys.argv) > 1 and sys.argv[1] == "-t":
    data1 = parse(f"test1.txt")
    data2 = parse(f"test2.txt")
else :
    inputFileName = f"input.txt"
    data2 = parse(inputFileName)
    data1 = parse(inputFileName)

answer1 = solve1(data1)
print(f"Answer1: {answer1}")
answer2 = solve2(data2)
print(f"Answer2: {answer2}")