class AStar:
    def __init__(self, dest, grid):
        self.dest = dest
        self.grid = self.abstractGrid(grid)
    #Will need another way of doing this so that the entire map isn't looped through every time
    #Maybe have a map of the collision tiles generated during map loadtime and then update the positions of the entities
    def abstractGrid(self, grid):
        abstract = []
        for y in range(len(grid)):
            for x in range(len(grid[0])):
                #Replace with ternary operator
                if grid[y][x].isCollidable:
                    pass
                else:
                    pass