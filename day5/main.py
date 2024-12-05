import sys

defaultDic = {"before":set(), "after":set()}

#parse input file into lines corresponding to the rules and the updates
def parse(inputFileName):
    rules = []
    updates =[]
    with open(inputFileName) as file:
        lines = file.readlines()
        splitingIndex = lines.index("\n")
        rules = lines[:splitingIndex]
        updates = lines[splitingIndex + 1 :]
        return rules, updates

# format a sting of the form "a.b.c.d\n" where here the delimiter is "." and a,b,c,d are ints
def format(lines, delimiter):
    result = []
    for s in lines:
        s = s.replace('\n', "").split(delimiter)
        result.append(list(map(lambda e:int(e), s)))
    return result
# format rules with delimiter "|"
def formatRules(unformatedRules):
    return format(unformatedRules, "|")

#format the updates with delimiter ","
def formatUpdates(unformatedUpdates):
    return format(unformatedUpdates, ",")

# Puzzles 

# Transforms the rules into a dictionary where each element indicates what should/could come after and before it
def getConstraintsFrom(rules):
    dic = {}
    for r in rules:
        # Add r[1] in the after set of r[0]
        previousValue0 = dic.get(r[0], defaultDic)
        dic[r[0]] = {"before":previousValue0["before"], "after":previousValue0["after"] | {r[1]}}
        # Add r[0] in the before set of r[1]
        previousValue1 = dic.get(r[1], defaultDic)
        dic[r[1]] = {"before":previousValue1["before"] | {r[0]}, "after":previousValue1["after"]}
    return dic

# Return 1)if the update is correct 2)the list of incorrect indexes if any
def wrongIndexInUpdate(constraints, update):
    notAllowed = set()
    indexes = []
    for i in range(len(update)):
        elem = update[i]
        if elem in notAllowed:
            indexes.append(i) 
        
        # Add everything that should be before the elem to notAllowed
        notAllowed = notAllowed.union(constraints.get(elem, defaultDic)["before"])
    return len(indexes) == 0, indexes
 
 # Correct the update given the set of constraint and the index of misplaced elements
def correctUpdate(constraints, update, wrongIndexes):
    for index in wrongIndexes:
        wrongElem = update[index]
        dicEntryForWrongElem = constraints.get(wrongElem, defaultDic)

        # move the wrongly placed element to the left and stop by verifying both its before set and the after set of 
        # the newly predecesor
        putHere = False
        i = index
        while (not putHere and i >= 0):
            i -= 1
            elemAtI = update[i]

            # The newly placed element appears in the new predecessor after set 
            # or the newly predecessor is in the before set of the newly placed element
            putHere = wrongElem in constraints.get(elemAtI, defaultDic)["after"] \
                or elemAtI in dicEntryForWrongElem["before"]
        del update[index]
        update.insert(i+1, wrongElem)
    return update
            

# Add the sum of middle element of correct updates or non correct ones (after correcting them) if onlyNonCorrect is set
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
