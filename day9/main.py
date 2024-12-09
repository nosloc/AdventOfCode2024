import sys


def parse(fileName):
    with open(fileName) as file:
        line = file.readline().strip()
        #print(len(line))
        return line
    
def multiplicativeSum(start, end, mult):
    indexes = list(range(start, end))
    #print(f"Adding {indexes} * {mult}")
    return mult * sum(indexes)


def solve1(line):
    front_id = 0
    front_index = 0
    back_id = (len(line)-1)//2
    back_index = len(line) - 1
    back_remaining_space = int(line[back_index])
    result_index = 0
    counter = 0
    while (True):
        # File space
        #print(f"Front {front_id}, index {front_index}")
        #print(f"back {back_id}, {back_remaining_space}, index {back_index}")
        #print(f"Handling file {front_id}")
        space = int(line[front_index])
        counter += multiplicativeSum(result_index, result_index+space, front_id)
        result_index += space
        front_id += 1
        front_index += 1
        
        # Free Space
        #print("Handling free space")
        space = int(line[front_index])
        fill_space = space == 0
        while not fill_space:
            #print(f"Indexes : {front_index, back_index}")
            start = result_index
            end = -1
            ID = back_id
            if (back_remaining_space >= space):
                #print("More remaining than space to fill")
                end = result_index+space
                result_index += space
                back_remaining_space -= space
                space = 0
                fill_space = True
            else :
                #print("Less space remaining than space to fill")
                end = result_index + back_remaining_space
                result_index += back_remaining_space
                space -= back_remaining_space
                back_remaining_space = 0
                fill_space = False
            
            if (back_remaining_space == 0):
                # Load next back number
                back_index -= 2
                back_id -= 1
                if not front_index >= back_index: 
                    back_remaining_space = int(line[back_index])
            counter += multiplicativeSum(start, end, ID)

            if(front_index >= back_index):
                #Exiting the loop
                fill_space = True
        #print()
        front_index +=1
        if (front_index >= back_index):
            if (back_remaining_space > 0):
                counter += multiplicativeSum(result_index, result_index+back_remaining_space, back_id)
            return counter


def processLine(line):
    res = [ [] for _ in range(10)]
    for i in range(len(line)-1, -1, -2):
        space = int(line[i])
        res[space].append(i)
    for l in res:
        l.append(-1)
    return res

def updateLastSeen(lastSeen, index):
    for i in range(1,len(lastSeen)):
        l = lastSeen[i]
        while (len(l) != 0):
            if l[0] >= index:
                print("removing :", l[0])
                l = l[1:]
            else :
                break
        lastSeen[i] = l
            


def solve2(line):
    line = list(line)
    already_seen = set()
    last_seen = processLine(line)
    #print(last_seen)
    front_index = 0
    result_index = 0
    counter = 0
    indexToId = lambda index: (index)//2
    while (True):
        # Handle file at front_id
        space = int(line[front_index])
        if (front_index not in already_seen):
            counter += multiplicativeSum(result_index, result_index+space, indexToId(front_index))
        result_index += space
        front_index += 1

        if (front_index >= len(line)-1):
            return counter 

        # Handle free space 

        space = int(line[front_index])
        still_space = space != 0
        while(still_space):
            index_of_fitting = max([l[0] for l in last_seen[:space+1]])
            if (index_of_fitting != -1 and index_of_fitting > front_index):
                back_space = int(line[index_of_fitting])
                #print(f"Find fitting space to fill {space}, space fitting {back_space, indexToId(index_of_fitting), index_of_fitting}")
                counter += multiplicativeSum(result_index, result_index+ back_space, indexToId(index_of_fitting))
                already_seen.add(index_of_fitting)
                last_seen[back_space] = last_seen[back_space][1:]
                space -= back_space
                result_index += back_space
                still_space = space != 0
                #print(result_index, space)
                #print(f"last_seen {last_seen}")
            else :
                still_space = False
                #print("None fitting")
        result_index += space
        front_index += 1


# Main 

inputFile = "input.txt"
if len(sys.argv)> 1 and sys.argv[1] == '-t':
    inputFile = "test2.txt"
line = parse(inputFile)
answer1 = solve1(line)
print(f"Answer1 : {answer1}")
answer2 = solve2(line)
print(f"Answer2 : {answer2}")