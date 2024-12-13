import sys

allDirections = [(-1,0), (0,1), (1,0), (0,-1)]

def getNextDirection(d):
    index = (allDirections.index(d) + 1) % len(allDirections)
    return allDirections[index]

def getPreviousDirection(d):
    index = (allDirections.index(d) - 1) % len(allDirections)
    return allDirections[index]

def parse(inputFile):
    with open(inputFile) as file:
        lines = file.readlines()
        return list(map(lambda s: s.replace("\n", ""), lines))

def solve1(garden):
    visited = set()
    height = len(garden)
    width = len(garden[0])
    inbound = lambda x,y: x >= 0 and x < height and y >= 0 and y < width
    result_counter = 0
    for x in range(height):
        for y in range(width):
            if ((x,y) not in visited):
                current_plot = garden[x][y]
                next_to_visit = [(x,y)]
                perimeter = 0
                area = 0
                while(len(next_to_visit)!=0):
                    #print(f"{current_plot}, {next_to_visit}, {perimeter}, {area}")
                    c_x, c_y = next_to_visit.pop(0)
                    area+=1
                    visited.add((c_x,c_y))
                    for dx, dy in allDirections:
                        x1, y1 = c_x + dx, c_y + dy
                        if inbound(x1,y1) and (garden[x1][y1] == current_plot):
                            if (x1, y1) not in visited and (x1, y1) not in next_to_visit:
                                next_to_visit.append((x1,y1))
                        else :
                            perimeter+=1
                #print(f"perimeter*area= {perimeter}*{area}= {perimeter*area}")
                result_counter += perimeter*area 
    return result_counter
            



def solve2(garden):
    visited = set()
    height = len(garden)
    #print(f"{height}")
    width = len(garden[0])
    inbound = lambda x,y: x >= 0 and x < height and y >= 0 and y < width
    result_counter = 0
    for x in range(height):
        for y in range(width):
            if ((x,y) not in visited):

                # The all zone
                current_plot = garden[x][y]

                # Count the area and the side if the tile is part of an boundary
                next_to_visit = [(x,y)]
                sides_tiles = set()
                area = 0
                nb_side = 0
                while(len(next_to_visit)!=0):
                    #print(f"{current_plot}, {next_to_visit}, {nb_side}, {area}")
                    c_x, c_y = next_to_visit.pop(0)
                    area+=1
                    visited.add((c_x,c_y))
                    for dx, dy in allDirections:
                        x1, y1 = c_x + dx, c_y + dy
                        if inbound(x1,y1) and (garden[x1][y1] == current_plot):
                            if (x1, y1) not in visited and (x1, y1) not in next_to_visit:
                                next_to_visit.append((x1,y1))
                        else : 
                            if (c_x, c_y) not in sides_tiles:
                                # Check the number of sides of this boudary
                                first_tile =(-1,-1)
                                first_direction = (-1,-1)
                                next_tile = (c_x,c_y)
                                curr_side = (dx, dy)
                                curr_direction = getNextDirection(curr_side)
                                first = True
                                # Find the perimeter : 
                                while not(curr_direction == first_direction and first_tile == next_tile):
                                    if first:
                                        first_tile = next_tile
                                        first_direction = curr_direction
                                        first = False
                                    #print(f"{next_tile}, {curr_direction}, {curr_side}")
                                    cur_x, cur_y = next_tile
                                    #if (c_x, c_y) not in visited:
                                    #    area += 1
                                    #    visited.add((c_x, c_y))
                                    # check boundary side 
                                    accross_boundary_x = cur_x+curr_side[0]
                                    accross_boundary_y = cur_y+curr_side[1]
                                    if (inbound(accross_boundary_x, accross_boundary_y)and \
                                                garden[accross_boundary_x][accross_boundary_y] == current_plot):
                                            curr_direction = curr_side
                                            curr_side = getPreviousDirection(curr_side)
                                            next_tile = (accross_boundary_x, accross_boundary_y)
                                            #print("adding a new side because of across boundary")
                                            nb_side +=1
                                            continue
                                    sides_tiles.add((cur_x, cur_y))
                                    along_dir_x = cur_x + curr_direction[0]
                                    along_dir_y = cur_y + curr_direction[1]
                                    if(not inbound(along_dir_x, along_dir_y) or \
                                        garden[along_dir_x][along_dir_y]!= current_plot):
                                        next_tile = (cur_x, cur_y)
                                        curr_direction = getNextDirection(curr_direction)
                                        curr_side = getNextDirection(curr_side)
                                        #print("adding a new side because of turning")
                                        nb_side += 1
                                    else:
                                        next_tile = (along_dir_x, along_dir_y)
                #print(f"perimeter*area= {perimeter}*{area}= {perimeter*area}")
                #print(area, nb_side)
                result_counter += nb_side*area
                #print(f"for {current_plot} the result_counter is {nb_side*area}")
    return result_counter
    
                    




# Main

inputFile = "input.txt"
if "-t" in sys.argv:
    inputFile = "test.txt"
garden = parse(inputFile)
answer1 = solve1(garden)
print(f"Answer1: {answer1}")
answer2 = solve2(garden)
print(f"Answer2: {answer2}")