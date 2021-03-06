import Tiles, Image, os, Main, CellularAutomata
from PIL import Image as Img
from random import choice
class Map():
    def __init__(self, path, tileSheetPath, animTileSheetPath):
        self.tileSheet = Image.SpriteSheet(tileSheetPath, 32)
        self.animTileSheet = Image.SpriteSheet(animTileSheetPath, 32)
        
        self.path = path
        
        #Cellular Automata test data
        self.cellheight = 40
        self.cellwidth = 40
    
    def getCavernTileMap(self):
        TileMap = []
        #chance = 0.6
        map, caverns = CellularAutomata.generateMap(self.cellwidth, self.cellheight, chance = 0.6, steps = 6, birthLimit = 3, deathLimit = 4)
        for rows in range(0, len(map)):
            row = []
            for columns in range(0, len(map[0])):
                if not map[rows][columns]:
                    row.append(Tiles.Tile((columns,rows), self.tileSheet.returnTile(0,0),False))
                else:
                    #row.append(Tiles.AnimTile((columns,rows), self.animTileSheet,True,0,3,10))
                    row.append(Tiles.Tile((columns, rows), self.tileSheet.returnTile(2, 0), True))
            TileMap.append(row)
        #Adds the tile that goes to next level
        EndLocation = choice(caverns[-2])
        TileMap[EndLocation[0]][EndLocation[1]] = Tiles.LevelTile((EndLocation[1],EndLocation[0]), self.tileSheet.returnTile(3,0), False)
        return TileMap, caverns
    
    def getTileMap(self):
        mapPath = Main.getPath(self.path)
        self.map = Img.open(mapPath)
        #Gets a list of all the pixel data in the img in a 1 dimensional list
        self.map = self.map.convert("RGB")
        pixels = list(self.map.getdata())
        #Sets the size so that the pixel list can be turned into a 2 dimensional array like a grid
        width, height = self.map.size
        pixels = [pixels[i * width:
            (i + 1) * width] for i in range(height)]
        self.pixels = pixels
        self.map.close()

        TileMap = []
        #columns then rows for 2D lists
        for y in range(0, len(self.pixels)):
            row = []
            for x in range(0, len(self.pixels[0])):
            #Tile format (Position, sprite, collision)
            #AnimTile format (gridPos, spritesheet,collision, animRow, NoOfFrames, timePeriod)
            #DamageTile format (gridPos, spritesheet, collision, animRow, NoOfFrames, timePeriod, damageValue)
            #TransportTile format (gridPos, sprite, collision, destination)
                #BLACK : Stone
                if self.pixels[y][x] == (0,0,0):
                    row.append(Tiles.Tile((x,y), self.tileSheet.returnTile(2,0),True))
                #RED : lava or generic damageTile
                elif self.pixels[y][x] == (255,0,0):
                    row.append(Tiles.DangerTileAnim((x,y), self.animTileSheet,False,1,3,20,1, cost = 100))
                #GREEN : grass
                elif self.pixels[y][x] == (0,255,0):
                    row.append(Tiles.Tile((x,y), self.tileSheet.returnTile(0,0),False))
                #BLUE : water
                elif self.pixels[y][x] == (0,0,255):
                    row.append(Tiles.AnimTile((x,y), self.animTileSheet,True,0,3,10))
                #YELLOW : Flowers
                elif self.pixels[y][x] == (255,255,0):
                    row.append(Tiles.Tile((x,y), self.tileSheet.returnTile(1,0),False))
                #MAGENTA : Transport
                elif self.pixels[y][x] == (255,0,255):
                    path = Main.getPath("res/map1.png")
                    row.append(Tiles.TransportTile((x,y), self.tileSheet.returnTile(3,0), False, path))
                #CYAN : ?
                elif self.pixels[y][x] == (0,255,255):
                    path = Main.getPath("res/map2.png")
                    row.append(Tiles.TransportTile((x,y), self.tileSheet.returnTile(3,0), False, path))
                #WHITE : ?
                elif self.pixels[y][x] == (255,255,255):
                    pass
                else:
                    print("Colour, ", self.pixels[x][y], "has no defining Tile")
            TileMap.append(row)
        return TileMap
    
    def getCellWidth(self):
        return self.cellwidth
    def getWidth(self):
        return len(self.pixels[0])
    def getCellHeight(self):
        return self.cellheight
    def getHeight(self):
        return len(self.pixels)
    def returnMap(self):
        return self.pixels

#Class for the map that will be randomly generated (incomplete)
class GeneratedMap:
    def __init__(self, rooms = None):
        self.WIDTH, self.HEIGHT = 100, 100
        self.GridRooms = []