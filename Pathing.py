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
                    node = Node(map[y][x].getCost(), y, x)
                    row.append(node)
                else:
                    row.append(None)
            graph.append(row)
        return graph
    def getNode(self, y, x):
        return self.grid[y][x]
        
class Node:
    def __init__(self, cost, y, x):
        self.cost = cost
        self.y = y
        self.x = x
              
    def neighbors(self, grid):
        dirs = [[1, 0], [0, 1], [-1, 0], [0, -1]]
        result = []
        for dir in dirs:
            try:
                if self.x == 0 or self.x == len(grid[0]): dir[1] == 0
                if self.y == 0 or self.y == len(grid): dir[0] == 0
                neighbor = grid[self.y + dir[0]][self.x + dir[1]]
            except IndexError:
               continue
            if neighbor is not None:
                result.append(neighbor)
        return result
    
    def getCost(self):
        return self.cost
      
    def __lt__(self, node):
        return self.getCost() < node.getCost()
    def __gt__(self, node):
        return self.getCost() < node.getCost()
   
#Astar      
#Probably need to refactor my code so that I have a list of cost integers rather than a list of objects that have a cost attribute
#Actually I definitaly do, idk why I thought that was a good idea
def heuristic(node1, node2):
   # Manhattan distance on a square grid
   return abs(node1.x - node2.x) + abs(node1.y - node2.y)
def FindPath(graph, dest, source):
    frontier = PriorityQueue()
    frontier.put(source, 0)
    came_from = {}
    cost_so_far = {}
    came_from[source] = None
    cost_so_far[source] = 0

    while not frontier.empty():
        current = frontier.get()

        if current == dest:
            break
        
        for next in current.neighbors(graph.grid):
            new_cost = cost_so_far[current] + current.getCost() + next.getCost()
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(dest, next)
                frontier.put(next, priority) 
                came_from[next] = current
    return reconstruct_path(came_from, source, dest)
def reconstruct_path(came_from, start, goal):
    current = goal
    path = []
    while current != start:
        path.append(current)
        try:
            current = came_from[current]
        except KeyError:
            pass
    #path.append(start) # optional
    path.reverse() # optional
    return path
