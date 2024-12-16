import sys
from enum import Enum
from collections import Counter



class Robot():
    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity
    
    def x(self):
        return self.position[0]
    def y(self):
        return self.position[1]
    def dx(self):
        return self.velocity[0]
    def dy(self):
        return self.velocity[1]
    def __repr__(self):
        return f"Robot({self.position}, {self.velocity})"
    
def parse(inputFileName):
    robots = []
    with open(inputFileName) as file:
        lines = file.readlines()
        for l in lines:
            position, vel = l.replace("\n", "").split()
            position = list(map(lambda s: int(s), position[2:].split(",")))
            vel = list(map(lambda s: int(s), vel[2:].split(",")))
            robots.append(Robot(position, vel))
    return robots

def position_at_time(robot, time, height, width):
    new_x = (robot.x() + robot.dx() * time)%width
    new_y = (robot.y() + robot.dy() * time)%height
    return new_x, new_y

def quadrant_onty(pos, height, width, middle_size):
    middle_size = middle_size //2
    return list(filter(lambda p: (p[0] > middle_size + width//2 \
                       or  p[0] < width//2-middle_size) \
                       and  (p[1] < height//2-middle_size \
                       or  p[1] > height//2+middle_size), pos.copy()))

def solve1(robots, height, width):
    return solve(robots, 100, 1, height, width)[1]


def solve(robots, time, quadrant_size, height, width):
    pos_at_time = list(map(lambda r: position_at_time(r, time, height, width), robots))
    top_left = 0
    top_right = 0
    bottom_right = 0
    bottom_left = 0
    quadrant_only = quadrant_onty(pos_at_time, height, width, quadrant_size)
    for x,y in quadrant_only:
        if (x < width//2):
            if (y < height//2):
                top_left += 1
            else:
                bottom_left += 1
        else:
            if (y < height//2):
                top_right += 1
            else:
                bottom_right += 1
    return  pos_at_time, top_right*top_left*bottom_left*bottom_right

def print_pos(positions, height, width):
    c = Counter(positions.copy())
    for j in range(height):
        for i in range(width):
            elem = c.get((i,j), 0)
            print(f"{elem if elem > 0 else " "} ", end="")
        print()

def solve2(robots, height, width):
    #for i in range(10000):
    #    pos, val = solve(robots, i, width - 35, height, width)
    #    if val <= 50:
    #        print(f"Iteration : {i}")
    #        print_pos(pos, height, width)
    found_result= 6668
    # If you want to print it
    #print_pos(list(map(lambda r: position_at_time(r, found_result, height, width), robots.copy())), height, width)
    return found_result






# Main
height = 103
width = 101
inputFile = "input.txt"
if "-t" in sys.argv:
    inputFile = "test.txt"
    height =7
    width = 11
robots = parse(inputFile)
answer1 = solve1(robots, height, width)
print(f"Answer1: {answer1}")
answer2 = solve2(robots, height, width)
print(f"Answer2: {answer2}")