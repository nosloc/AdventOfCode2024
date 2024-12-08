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
def isValid(res, nums, allowConc=False, prefix=""):
    #print(f"{prefix}isValid({res, nums, allowConc})")
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
            if (isValid(res//lastNum, remaining, allowConc, prefix=prefix+'\t')):
                return True
        if (allowConc):
            #print(f"{prefix} trying conc")
            l = len(str(lastNum))
            part2 = res%(10**l)
            part1 = res//(10**l)
            if(part2==lastNum):
                if isValid(part1, remaining, allowConc, prefix=prefix+'\t'):
                    return True
        #print(f"{prefix}trying minus")
        return isValid(res-lastNum, remaining, allowConc, prefix= prefix + "\t")

def solve(equations, allowConc=False):
    counter = 0
    for e in equations:
        res = e["Result"]
        nums = e["Numbers"]
        if isValid(res, nums, allowConc):
            counter += res
    return counter

# Main
inputFile = "input.txt"
if len(sys.argv)> 1 and sys.argv[1] == '-t':
    inputFile = "test.txt"
lines = parse(inputFile)
parts = format(lines)
answer1 = solve(parts)
print(f"Answer1 : {answer1}")
answer2 = solve(parts, True)
print(f"Answer2 : {answer2}")