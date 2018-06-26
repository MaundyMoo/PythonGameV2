import os, pygame
from PIL import Image as Img
#This function returns a pygame styled image from a directory that can then be drawn onto the surface
def getImage(path):
    image_library = {}
    image = image_library.get(path)
    if image == None:
            canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
            image = pygame.image.load(canonicalized_path).convert()
            image_library[path] = image
    return image
#This function returns the version of the image that will be displayed when an entity takes damage, put in this scope as it involves image manipulation
def spriteFlash(spr, colour):
    for each in spr.getdata():
        #print(each)
        pass
        
class SpriteSheet:
    def __init__(self, path, spriteSize):
        self.spriteSize = spriteSize
        self.sheet = Img.open(path)
        self.sheet = self.sheet.convert('RGBA')
        self.removeColour(list(self.sheet.getdata()))
        self.TileSheet = self.getTiles()
        self.sheet.close()
    #Returns a grid of tiles in PIL png format
    def getTiles(self):
        tiles = []
        pixels = list(self.sheet.getdata())
        width, height = self.sheet.size
        pixels = [pixels[i * width:
            (i + 1) * width] for i in range(height)]
        for y in range(0, int(len(pixels) / self.spriteSize) + 1):
            row = []
            for x in range(0, int(len(pixels[0]) / self.spriteSize) + 1):
                tile = self.sheet.crop((x * self.spriteSize,y * self.spriteSize,(x * self.spriteSize)+self.spriteSize,(y * self.spriteSize)+self.spriteSize))
                row.append(tile)
            tiles.append(row)
        return tiles
    #Removes certain colours from the spritesheet #FF00FF, #880088 are removed
    def removeColour(self, image):
        width, height = self.sheet.size
        image = [image[i * width:
            (i + 1) * width] for i in range(height)]
        for y in range(0,len(image)):
            for x in range(0, len(image[0])):
                #If the detected colour is #FF00FF or #880088, replace it with a transparent white pixel 
                if image[y][x] == (255, 0, 255, 255) or image[y][x] == (136, 0, 136, 255):
                    self.sheet.putpixel((x,y), (255, 255, 255, 0))
    def returnTile(self, x, y):
        return self.TileSheet[y][x]