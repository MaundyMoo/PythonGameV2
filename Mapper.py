import Tiles, Image
from PIL import Image as Img
class Map():
    def __init__(self, mapPath, tileSheetPath, animTileSheetPath):
        self.map = Img.open(mapPath)
        self.tileSheet = Image.SpriteSheet(tileSheetPath, 32)
        self.animTileSheet = Image.SpriteSheet(animTileSheetPath, 32)
        #Gets a list of all the pixel data in the img in a 1 dimensional list
        self.map = self.map.convert("RGB")
        pixels = list(self.map.getdata())
        #Sets the size so that the pixel list can be turned into a 2 dimensional array like a grid
        width, height = self.map.size
        pixels = [pixels[i * width:
            (i + 1) * width] for i in range(height)]
        self.pixels = pixels
        #self.TileMap = self.getTileMap()
        self.map.close()
    def getTileMap(self):
        TileMap = []
        #columns then rows for 2D lists
        for y in range(0, len(self.pixels)):
            row = []
            for x in range(0, len(self.pixels[0])):
            #Tile format (Position, sprite, collision, destructable)
                #BLACK : Stone
                if self.pixels[y][x] == (0,0,0):
                    row.append(Tiles.Tile((x,y),self.tileSheet.returnTile(0,1),True))
                #RED : lava or smth?
                elif self.pixels[y][x] == (255,0,0):
                    row.append(Tiles.DangerTileAnim((x,y),self.animTileSheet,False,1,3,20, 5))
                #GREEN : grass
                elif self.pixels[y][x] == (0,255,0):
                    row.append(Tiles.Tile((x,y),self.tileSheet.returnTile(0,0),False))
                #BLUE : water
                elif self.pixels[y][x] == (0,0,255):
                    row.append(Tiles.AnimTile((x,y),self.animTileSheet,True,0,3,10))
                #YELLOW : Flowers?
                elif self.pixels[y][x] == (255,255,0):
                    row.append(Tiles.Tile((x,y),self.tileSheet.returnTile(1,0),False))
                #MAGENTA : ?
                elif self.pixels[y][x] == (255,0,255):
                    pass
                #CYAN : ?
                elif self.pixels[y][x] == (0,255,255):
                    pass
                #WHITE : ?
                elif self.pixels[y][x] == (255,255,255):
                    pass
                else:
                    print("Colour, ", self.pixels[x][y], "has no defining Tile")
            TileMap.append(row)
        return TileMap
    def getWidth(self):
        return len(self.pixels[0])
    def getHeight(self):
        return len(self.pixels)
    def returnMap(self):
        return self.pixels