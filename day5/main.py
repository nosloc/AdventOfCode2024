import sys

defaultDic = {"before":set(), "after":set()}

def parse(inputFileName):
    rules = []
    updates =[]
    with open(inputFileName) as file:
        lines = file.readlines()
        splitingIndex = lines.index("\n")
        rules = lines[:splitingIndex]
        updates = lines[splitingIndex + 1 :]
        return rules, updates

def format(lines, delimiter):
    result = []
    for s in lines:
        s = s.replace('\n', "").split(delimiter)
        result.append(list(map(lambda e:int(e), s)))
    return result

def formatRules(unformatedRules):
    return format(unformatedRules, "|")

def formatUpdates(unformatedUpdates):
    return format(unformatedUpdates, ",")

# Puzzle 1

def getConstraintsFrom(rules):
    dic = {}
    for r in rules:
        previousValue0 = dic.get(r[0], defaultDic)
        dic[r[0]] = {"before":previousValue0["before"], "after":previousValue0["after"] | {r[1]}}
        previousValue1 = dic.get(r[1], defaultDic)
        dic[r[1]] = {"before":previousValue1["before"] | {r[0]}, "after":previousValue1["after"]}
    return dic

def wrongIndexInUpdate(constraints, update):
    notAllowed = set()
    indexes = []
    for i in range(len(update)):
        elem = update[i]
        if elem in notAllowed:
            indexes.append(i) 
        notAllowed = notAllowed.union(constraints.get(elem, defaultDic)["before"])
    return len(indexes) == 0, indexes

def correctUpdate(constraints, update, wrongIndexes):
    for index in wrongIndexes:
        wrongElem = update[index]
        dicEntryForWrongElem = constraints.get(wrongElem, defaultDic)
        putHere = False
        i = index
        while (not putHere and i >= 0):
            i -= 1
            elemAtI = update[i]
            putHere = wrongElem in constraints.get(elemAtI, defaultDic)["after"] \
                or elemAtI in dicEntryForWrongElem["before"]
        del update[index]
        update.insert(i+1, wrongElem)
    return update
            


def solve(rules, updates, onlyNonCorrect):
    constraintDict = getConstraintsFrom(rules)
    counter = 0
    for update in updates:
        valid, indexes = wrongIndexInUpdate(constraintDict, update)
        if onlyNonCorrect and not valid:
            update = correctUpdate(constraintDict, update, indexes)
            counter += update[len(update)//2]
        elif valid and not onlyNonCorrect:
            counter += update[len(update)//2]

    return counter

# Main

inputFileName = "input.txt"
if len(sys.argv) > 1 and sys.argv[1] == "-t":
    inputFileName = "test.txt"
rules, updates = parse(inputFileName)
rules = formatRules(rules)
updates = formatUpdates(updates)
answer1 = solve(rules, updates, False)
print(f"Anser1 : {answer1}")
answer2 = solve(rules, updates, True)
print(f"Answer2 : {answer2}")
