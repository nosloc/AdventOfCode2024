import sys
from enum import Enum
from functools import reduce

class Direction(Enum):
    Up = '^'
    Down = 'v'
    Right = '>'
    Left = '<'

def get_Value(dir):
    if dir == Direction.Up:
        return -1, 0
    if dir == Direction.Down:
        return 1, 0
    if dir == Direction.Left:
        return 0, -1
    if dir == Direction.Right:
        return 0, 1

wall = "#"
empty = "."
robot = "@"
obj = "O"
box1 = "["
box2 = "]"
class Map1():
    def __init__(self, m):
        self.height = len(m)
        self.width = len(m[0])
        self.m = []
        self.robot_pos = (-1,-1)
        i = 0
        for l in m:
            l = list(l)
            if robot in l:
                self.robot_pos = (i, l.index(robot))
                l[self.robot_pos[1]] = empty
            self.m.append(l)
            i += 1
    def __repr__(self):
        ret = ""
        for i in range(self.height):
            line = self.m[i]
            for j in range(len(line)):
                if (i, j) == self.robot_pos:
                    ret += robot
                else :
                    ret += line[j]
            ret += "\n"
        return ret
    
    def move_bot(self, dir):
        x, y = self.robot_pos
        dx, dy = get_Value(dir)
        self.move(x,y,dx,dy,is_bot=True)

    def move(self, x, y, dx, dy, is_bot = False):
        c = self.m[x][y]
        if (c == wall or (c == empty and not is_bot)):
            return False
        else :
            n = self.m[x + dx][y + dy]
            if n == wall :
                return False
            else:
                can_move = n==empty or self.move(x+dx, y+dy, dx, dy)
                if can_move:
                    if is_bot: 
                        self.m[x][y] = empty
                        self.m[x + dx][y + dy] = empty
                        self.robot_pos = (x + dx, y + dy)
                    else :
                        self.m[x + dx][y + dy] = c
                    return True
                else :
                    return False
    def get_sum_boxes(self):
        counter = 0
        for x in range(1, self.height-1):
            line = self.m[x]
            for y in range(1, self.width-1):
                c = line[y]
                if c == obj:
                    counter += x * 100 + y
        return counter


class Map2():
    def __init__(self, m):
        self.height = len(m)
        self.width = len(m[0])*2
        self.m = []
        self.robot_pos = (-1,-1)
        i = 0
        for l in m:
            l = list(l)
            if robot in l:
                self.robot_pos = (i, l.index(robot)*2)
                l[l.index(robot)] = empty
            self.m.append(list(reduce(lambda a,b: a+b, list(map(lambda c: [box1,box2] if c == obj else [c,c], l)))))
            i += 1
    def __repr__(self):
        ret = ""
        for i in range(self.height):
            line = self.m[i]
            for j in range(len(line)):
                if (i, j) == self.robot_pos:
                    ret += robot
                else :
                    ret += line[j]
            ret += "\n"
        return ret
    
    def move_bot(self, dir):
        x, y = self.robot_pos
        dx, dy = get_Value(dir)
        self.move(x,y,dx,dy,is_bot=True)

    def move(self, x, y, dx, dy, is_bot = False):
        c = self.m[x][y]
        if (c == wall or (c == empty and not is_bot)):
            return False
        nexts_pos = [(x+dx,y+dy)]
        nexts = [self.m[i][j] for i,j in nexts_pos]
        if (nexts[0] == box1 and dx != 0):
            nexts_pos.append((x+dx, y+dy+1))
        elif (nexts[0] == box2 and dx != 0):
            nexts_pos.insert(0, (x+dx, y+dy-1))

        nexts = [self.m[i][j] for i,j in nexts_pos]
        if wall in nexts:
            return False
        else:
            nexts = list(zip(nexts_pos, nexts))
            m_copy = [l.copy() for l in self.m]
            for i in range(len(nexts)):
                n = nexts[i]
                n_pos = n[0]
                n_value = n[1]
                if not (n_value == empty or self.move(n_pos[0], n_pos[1], dx, dy)):
                    # Reversing any moves that should not have been done
                    self.m = m_copy
                    return False
            if is_bot: 
                self.m[x][y] = empty
                self.m[x + dx][y + dy] = empty
                self.robot_pos = (x + dx, y + dy)
            else :
                self.m[x + dx][y + dy] = self.m[x][y]
                self.m[x][y] = empty
            return True

    def get_sum_boxes(self):
        counter = 0
        for x in range(1, self.height-1):
            line = self.m[x]
            for y in range(1, self.width-1):
                c = line[y]
                if c == box1:
                    counter += x * 100 + y
        return counter





def parse(fileName):
    moves = []
    my_map = []
    is_moves = False
    with open(fileName) as file:
        lines = file.readlines()
        for l in lines:
            if l == "\n":
                is_moves = True
            else :
                l= l.replace("\n", "")
                if is_moves:
                    for c in l:
                        m = Direction(c)
                        moves.append(m)
                else :
                    my_map.append(l)
    return my_map, moves

def solve1(m, moves):
    m = Map1(m) 
    for move in moves:
        #print(move)
        m.move_bot(move)
    print("Conf after all moves")
    print(m)
    return m.get_sum_boxes()

def solve2(m, moves):
    m = Map2(m) 
    #print(m)
    for move in moves:
        #print(move)
        m.move_bot(move)
        #print(m)
    print("\nLast map after the bot stop moving")
    print(m)
    return m.get_sum_boxes()

# Main
inputFile = "input.txt"
if "-t" in sys.argv:
    index = sys.argv.index("-t") + 1
    number = 1
    if (index< len(sys.argv)):
        number = sys.argv[index]
    inputFile = f"test{number}.txt"
m, moves = parse(inputFile)
answer1 = solve1(m, moves)
print(f"Answer1: {answer1}")
answer2 = solve2(m, moves)
print(f"Answer2: {answer2}")