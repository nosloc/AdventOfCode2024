import sys

#Puzzle 1
def parse(inputFile):
    file = open(inputFile)
    lines = map(lambda s: s.split(), file.readlines())
    list1 = []
    list2 = []
    for a,b in lines:
        list1.append(int(a))
        list2.append(int(b))
    list1.sort()
    list2.sort()
    return list1, list2

def solve1(l1,l2):
    dist_counter = 0
    for i in range(len(l1)):
        dist_counter += abs(l1[i]-l2[i])
    return dist_counter


# Puzzle 2

def createDir(l):
    dic = {}
    return dic

def solve2(l1,l2):
    dic2 = {}
    
    for i in l2:
        value = dic2.get(i)
        if value == None:
            dic2[i]=1
        else :
            dic2[i] = value+1

    similarityCounter=0
    for index in l1:
        c2 = dic2.get(index)
        if c2 != None:
            similarityCounter += index * c2
    return similarityCounter

# Main 

DEFAULT_PATH = "inputs/day1/"
inputFileName = "input.txt"
if len(sys.argv) >= 2:
    if sys.argv[1] == "-t":
        inputFileName = "test.txt"

l1, l2 = parse(DEFAULT_PATH + inputFileName)
answer1 = solve1(l1,l2)
print(f"Answer 1: {answer1}")
answer2 = solve2(l1,l2)
print(f"Answer 2: {answer2}")
