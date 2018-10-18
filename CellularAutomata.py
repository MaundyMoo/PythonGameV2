'''
    Cellular Automata Test
'''
from random import random
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
def generateMap(width = 50, height = 50, chance = 0.5, steps = 1, birthLimit = 4, deathLimit = 4):
    map = generateRandomMap(width, height, chance)
    for i in range(0, steps+1):
        map = stepSimulation(map, birthLimit, deathLimit)
    return map
'''
map = generateRandomMap(50,50,0.5)
for each in map:
    print(each)
'''