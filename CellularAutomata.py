'''
    Cellular Automata Test
'''
from random import random
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
    cavernMap = []
    #Unnescesary looping through list, will remove after complete, just helps for visualisation 
    for y in range(0, len(map)):
        row = []
        for x in range(0, len(map[0])):
            if map[y][x]:
                row.append(',')
            else:
                row.append('.')
        cavernMap.append(row)
    counter = 0
    for y in range(0, len(cavernMap)):
        for x in range(0, len(cavernMap[0])):
            if cavernMap[y][x] == '.':
                cavernMap = floodfill((y,x), cavernMap, counter)
                counter += 1
    for each in cavernMap:
        print(each)
def floodfill(location: tuple, map: list, cavernNo: int):
    y, x = location
    if not map[y][x] == '.':
        print("Something went wrong") 
    #Cast to a string to make debug easier as everything will print uniformly then
    map[y][x] = str(cavernNo)
    if not y == len(map)-1:
        if map[y+1][x] == '.': floodfill((y+1, x), map, str(cavernNo))
    if not y == 0:
        if map[y-1][x] == '.': floodfill((y-1, x), map, str(cavernNo))
    if not x == len(map[0])-1:
        if map[y][x+1] == '.': floodfill((y, x+1), map, str(cavernNo))
    if not x == 0:
        if map[y][x-1] == '.': floodfill((y, x-1), map, str(cavernNo))
    return map
#Driver function for running the necessary procedures to generate a map
def generateMap(width = 50, height = 50, chance = 0.5, steps = 1, birthLimit = 4, deathLimit = 4):
    map = generateRandomMap(width, height, chance)
    for i in range(0, steps+1):
        map = stepSimulation(map, birthLimit, deathLimit)
    getCaverns(map)
    return map