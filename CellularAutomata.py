'''
    Cellular Automata Test
'''
from random import random, choice

#Creates/Seeds a random 2D array with true or false values for alive or dead cells
def generateRandomMap(width: int, height: int, chance: float) -> list:
    map = []
    for y in range(0, height):
        row = []
        for x in range(0, width):
            if random() < chance:
                tile = False
            else:
                tile = True
            row.append(tile)
        map.append(row)
    return map
#Iterates through each cell and determines whether it lives or dies and creates a new map based on this  
def stepSimulation(map: list, deathLimit: int, birthLimit: int):
    newMap = map
    for y in range(0, len(map)):
        for x in range(0, len(map[0])):
            neighbours = countLivingNeighbours(map, x, y)
            if map[y][x]:
                if neighbours < deathLimit:
                    newMap[y][x] = False
                else:
                    newMap[y][x] = True
            else:
                if neighbours > birthLimit:
                    newMap[y][x] = True
                else:
                    newMap[y][x] = False
    return newMap
#Returns the number of neighbours a cell has, used for calculating whether a cell lives or dies
def countLivingNeighbours(map: list, x: int, y: int):
    count = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            neighbourX = x + i
            neighbourY = y + j
            if i == 0 and j == 0:
                pass
            elif neighbourX < 0 or neighbourY < 0 or neighbourX >= len(map[0]) or neighbourY >= len(map):
                count += 1
            elif map[neighbourY][neighbourX]:
                count += 1
    return count
#Uses floodfill algorithm to determine the caverns within the map
def getCaverns(map: list):
    '''
    In this sequence of steps to floodfill the caverns and try to connect them, I loop through the map WAAAAAY too many times, will need a fair amount 
    of refactoring for this to be anywhere near 
    a) optimised for performance
    b) will need editing to have more functions, because currently the floodfill isn't used for counting the size of the caverns which could be useful
    '''
    cavernMap = []
    #Unnescesary looping through list, will remove after complete, just helps for visualisation 
    for y in range(0, len(map)):
        row = []
        for x in range(0, len(map[0])):
            if map[y][x]:
                row.append(',') #wall is true
            else:
                row.append('.')
        cavernMap.append(row)
    #Used to count the number of caverns
    counter = 0
    for y in range(0, len(cavernMap)):
        for x in range(0, len(cavernMap[0])):
            if cavernMap[y][x] == '.':
                cavernMap = floodfill((y,x), cavernMap, counter)
                counter += 1
    #Gets the position of every open tile in a cavern
    caverns = []
    for i in range(0, counter+1):
        temp = []
        for y in range(0, len(cavernMap)):
            for x in range(0, len(cavernMap[0])):
                if cavernMap[y][x] == str(i):
                    temp.append((y,x))
        caverns.append(temp)
    if len(caverns) > 1:
        #Loop through cavern locations and make sure two adjaceantly numbered caverns are connected
        for i in range(0, len(caverns)-2):
            map = joinCaverns(choice(caverns[i]), choice(caverns[i+1]), cavernMap)
    for each in map:
        print(each)
    print('-' * 200)
    for y in range(0, len(map)):
        for x in range(0, len(map[0])):
            if cavernMap[y][x] == ',':
                cavernMap[y][x] = True
            else:
                cavernMap[y][x] = False
    return cavernMap, caverns
def floodfill(location: tuple, map: list, cavernNo: int, cavernSize = 0):
    y, x = location
    #Cast to a string to make debug easier as everything will print uniformly then
    map[y][x] = str(cavernNo)
    if not y == len(map)-1:
        if map[y+1][x] == '.': cavernSize+=1;floodfill((y+1, x), map, str(cavernNo),cavernSize)
    if not y == 0:
        if map[y-1][x] == '.': cavernSize+=1;floodfill((y-1, x), map, str(cavernNo),cavernSize)
    if not x == len(map[0])-1:
        if map[y][x+1] == '.': cavernSize+=1;floodfill((y, x+1), map, str(cavernNo),cavernSize)
    if not x == 0:
        if map[y][x-1] == '.': cavernSize+=1;floodfill((y, x-1), map, str(cavernNo),cavernSize)
    return map
#Join caverns maybe? could prolly just do in get caverns function, do I need more abstraction from myself?
def joinCaverns(cavern1: tuple, cavern2: tuple, map: list):
    y1, x1 = cavern1
    y2, x2 = cavern2
    #Connect on x axis
    if x1 < x2:
        for i in range(x1, x2+1):
            map[y1][i] = 'a'
    elif x1 > x2:
        for i in range(x2, x1+1):
            map[y1][i] = 'b'
    if y1 < y2:
        for i in range(y1, y2+1):
            map[i][x2] = 'c'
    elif x1 > x2:
        for i in range(y2, y1+1):
            map[i][x2] = 'd'
    return map
#Driver function for running the necessary procedures to generate a map
def generateMap(width = 50, height = 50, chance = 0.5, steps = 1, birthLimit = 4, deathLimit = 4):
    map = generateRandomMap(width, height, chance)
    for i in range(0, steps+1):
        map = stepSimulation(map, birthLimit, deathLimit)
    map, caverns = getCaverns(map)
    return map, caverns