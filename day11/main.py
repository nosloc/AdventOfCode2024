import sys

        
                

# Debug print
def debugPrint(s):
    if debug:
        print(f"{s}")

def parse(inputFile):
    with open(inputFile) as file:
        line = file.readline().replace("\n", "").split()
        result_dic = {}
        for c in line:
            result_dic[int(c)]=result_dic.get(int(c), 0) + 1
        return result_dic
        
def countNumbersOfStone(initial_state, blinks):
    dic = initial_state
    next_dic = {}
    for _ in range(blinks):
        debugPrint(dic)
        for (value, number) in dic.items():
            res = getNextState(value)
            for i in res:
                next_dic[i] = next_dic.get(i, 0)+number
        dic = next_dic.copy()
        next_dic = {}
    return sum(dic.values())
        
        
def getNextState(number):
    s = str(number)
    #debugPrint(f"getting next state of {number}")
    if (number == 0):
        return [1]
    if len(s) % 2 == 0:
        middlePoint = len(s)//2
        return [int(s[:middlePoint]), int(s[middlePoint:])]
    else :
        return [number*2024]
def solve(input, blinks):
    return countNumbersOfStone(input, blinks)



    
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

blinks = 25
dic = parse(inputFile)
answer1 =solve(dic, blinks)
print("Answer1: ", answer1)
blinks = 75 
answer2 = solve(dic, blinks)
print(f"Answer2 : {answer2}")