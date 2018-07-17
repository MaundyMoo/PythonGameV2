class AStar:
    def __init__(self, dest: tuple, grid: list):
        self.dest = dest
        self.xDest = dest[0]
        self.yDest = dest[1]
        self.grid = self.abstractGrid(grid)
        
    def abstractGrid(self, grid: list) -> list:
        #Will need another way of doing this so that the entire map isn't looped through every time
        #Maybe have a map of the collision tiles generated during map loadtime and then update the positions of the entities
        #Add various values based on whther tile would damage or not so that mobs prioritise safe tiles over damaging tiles
        abstract = []
        for y in range(len(grid)):
            row = []
            for x in range(len(grid[0])):
                #Replace with ternary operator at some point because it might be slightly faster idk
                if grid[y][x].isCollidable():
                    row.append(1)
                else:
                    row.append(0)
            abstract.append(row)
        return abstract
#Im not too sure if I'll need a node object but it's here just in case
class Node:
    def __init__(self):
        pass