#from Queue import PriorityQueue
#Turn Map into a grid made of nodes where walkable tiles become nodes / edges
#I dont know how to make edges D:
from queue import PriorityQueue
#from Main import WIDTH, HEIGHT
#from Tiles import TILESIZE
class Graph():
    def __init__(self, tileMap):
        self.grid = self.generateGraph(tileMap)
    def generateGraph(self, map):
        graph = []
        for y in range(0, len(map)):
            row = []
            for x in range(0, len(map[0])):
                if not map[y][x].isCollidable():
                    row.append([x, y, map[y][x].getCost()])
                else:
                    row.append(None)
            graph.append(row)
        return graph
    #node argument is a 1D list from the 2D graph, attempting this way rather than using the previous method of node objects as iterating through python objects, I believe, is slower than iterating over simple lists and ints
    def neighbours(self, node: list) -> list:
        dirs = [[1, 0], [0, 1], [-1, 0], [0, -1]]
        result = []
        for dir in dirs:
            neighbour = [node[0] + dir[0], node[1] + dir[1]]
            #Bounds the edges to within the grid
            if 0 <= neighbour[0] < len(self.grid) and 0 <= neighbour[1] < len(self.grid[0]) and not self.getCost(neighbour) == None:
                result.append([node[0] + dir[0], node[1] + dir[1]])
        return result
    def getCost(self, node):
        try:
            return self.grid[node[0]][node[1]][2]
        except TypeError:
            return None           
            
    #TODO make this fit to my code: Fix the list dictionary issue or rewrite Astar my own way
    def heuristic(self, a, b):
        (x1, y1) = a
        (x2, y2) = b
        return abs(x1 - x2) + abs(y1 - y2)

    def Astar(self, start, goal):
        frontier = PriorityQueue()
        frontier.put(start, 0)
        came_from = {}
        cost_so_far = {}
        came_from[start] = None
        cost_so_far[start] = 0
        
        while not frontier.empty():
            current = frontier.get()
            
            if current == goal:
                break
            
            for next in self.neighbours(current):
                new_cost = cost_so_far[current] + self.getCost(next)
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + self.heuristic(goal, next)
                    frontier.put(next, priority)
                    came_from[next] = current
        
        return self.reconstruct_path(came_from, start, goal) #came_from, cost_so_far 

    def reconstruct_path(self, came_from, start, goal):
        current = goal
        path = []
        while current != start:
            path.append(current)
            current = came_from[current]
        path.append(start) # optional
        path.reverse() # optional
        return 