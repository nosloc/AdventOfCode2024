import sys

def parse(input_file):
    paterns = set()
    designs = []
    with open(input_file) as file:
        paterns = set([s.replace("\n", "") for s in file.readline().split(", ")])
        assert(file.readline() == "\n")
        designs = [s.replace("\n", "") for s in file.readlines()]
        return paterns, designs

def count(paterns, d, already_counted, all_possibilities):
    if d == "":
        return 1
    res = already_counted.get(d, None)
    if res != None:
        return res
    counter = 0
    for p in paterns: 
        if d.startswith(p):
            res = count(paterns, d[len(p):], already_counted, all_possibilities)
            if not all_possibilities and res > 0:
                return 1
            else:
                counter += res 
    # print(f"Adding {d} -> {counter}")
    already_counted[d] = counter
    return counter

def solve(paterns, designs, all_possibilities):
    counter = 0
    already_counted = {}
    if not all_possibilities:
        for p in paterns:
            already_counted[p] = 1
    for d in designs:
        counter += count(paterns, d, already_counted, all_possibilities)
    return counter



input_file = "input.txt"
if  "-t" in sys.argv :
    input_file = "test.txt"
paterns, designs = parse(input_file)
answer1 = solve(paterns, designs, False)
print(f"Answer 1: {answer1}")
answer2 = solve(paterns, designs, True)
print(f"Answer 2: {answer2}")
