import sys

def parse(inputFileName):
    with open(inputFileName) as file:
        return list(map(lambda s: s.replace('\n', ""), file.readlines()))
def format(lines):
    parts = list(map(lambda s: s.split(':'), lines))
    parts = list(map(lambda l: (int(l[0]), list(map(lambda s: int(s),l[1].strip().split(" ")))), parts))
    parts = list(map(lambda tup: {"Result": tup[0], "Numbers": tup[1]}, parts))
    return parts


# Puzzle 1 
def isValid(res, nums, prefix=""):
    #print(f"{prefix}isValid({res, nums, allowConcatenation})")
    l = len(nums)
    if l == 0:
        return False
    if l == 1:
        return res == nums[0]
    else:
        lastNum = nums[-1]
        remaining = nums[:-1]

        # Handle this case since it false the next one
        if (lastNum == 0 and res == 0):
            return True
        #If the res mod lastNum != 0 the the last operation can't be a *
        if (res%lastNum == 0):
            #print(f"{prefix}Trying div")
            if (isValid(res//lastNum, remaining, prefix=prefix+'\t')):
                return True
        #print(f"{prefix}trying minus")
        return isValid(res-lastNum, remaining, prefix= prefix + "\t")

def solve(equations):
    counter = 0
    for e in equations:
        res = e["Result"]
        nums = e["Numbers"]
        if isValid(res, nums):
            counter += res
    return counter

def isValidBruteForce(res, sofar, numbers, first=False, prefix=""):
    #print(f"{prefix}res={res}, sofar={sofar}, numbers={numbers}")
    if len(numbers)==0:
        return sofar==res
    if sofar > res:
        return False
    # Multiplication
    newSofar = sofar if not first else 1
    if isValidBruteForce(res, newSofar*numbers[0], numbers[1:], prefix=prefix+"\t"):
        return True
    # Concatenation
    newSofar = int(str(sofar)+str(numbers[0]))
    if isValidBruteForce(res, newSofar, numbers[1:], prefix=prefix+"\t"):
        return True
    # Addition
    if isValidBruteForce(res, sofar+numbers[0], numbers[1:], prefix=prefix+"\t"):
        return True
    return False


def solve2(equations):
    counter = 0
    i = 0
    l = len(equations)
    for e in equations:
        i+=1
        print(f"Progress {i/l*100:.2f}%", end="\r")
        res = e["Result"]
        nums = e["Numbers"]
        if isValidBruteForce(res, 0, nums, first=True):
            counter += res
        #print()
    print()
    return counter


# Main
inputFile = "input.txt"
if len(sys.argv)> 1 and sys.argv[1] == '-t':
    inputFile = "test.txt"
lines = parse(inputFile)
parts = format(lines)
answer1 = solve(parts)
print(f"Answer1 : {answer1}")
answer2 = solve2(parts)
print(f"Answer2 : {answer2}")