import Image, pygame, Main
tileSize = TILESIZE = 32
class Tile:
    #Tiles will always be square
    TILESIZE = tileSize
    def __init__(self, gridPos: tuple, sprite, collision: bool, cost = 1):
        #Pygame cannot natively read PIL png formats, so have to convert to string to let pygame read it
        self.sprite = pygame.image.fromstring(sprite.tobytes(), sprite.size, sprite.mode)
        self.sprite = pygame.transform.scale(self.sprite, (self.TILESIZE, self.TILESIZE))
        #Boolean flags
        self.collision = collision  

        self.cost = cost    
        
        self.pos = gridPos
    def Render(self, screen, OffsetX: int, OffsetY: int):
        screen.blit(self.sprite, ((self.pos[0] * self.TILESIZE) + OffsetX, (self.pos[1] * self.TILESIZE) + OffsetY))
    def Update(self):
        pass
    def isCollidable(self) -> bool:
        return self.collision
    def getCost(self):
        return self.cost
class AnimTile(Tile):
    def __init__(self, gridPos: tuple, spritesheet: str, collision: bool, animRow: int, NoOfFrames: int, timePeriod: int, cost :int = 0):
        self.NoOfFrames = NoOfFrames
        self.timePeriod = timePeriod
        self.spriteSheet = spritesheet
        self.animRow = animRow
        #Tile needs an initial sprite to set the attribute sprite
        initialSprite = self.spriteSheet.returnTile(0, self.animRow)
        super().__init__(gridPos, initialSprite, collision, cost)
        self.tick = 0
        
    def Render(self, screen, OffsetX, OffsetY):
        self.tick += 1
        cycleTime = (self.NoOfFrames + 1) * self.timePeriod - 1
        if self.tick > cycleTime:
            self.tick = 0
        self.sprite = self.ImgToSprite(self.spriteSheet.returnTile(self.tick // self.timePeriod, self.animRow))
        screen.blit(self.sprite, ((self.pos[0] * self.TILESIZE) + OffsetX, (self.pos[1] * self.TILESIZE) + OffsetY))
    def ImgToSprite(self, spr):
        Sprite = pygame.image.fromstring(spr.tobytes(), spr.size, spr.mode)
        Sprite = pygame.transform.scale(Sprite, (self.TILESIZE, self.TILESIZE))
        return Sprite
#Special non floor / wall tiles could go here that would need special parameters i.e. door that needs destination
class DangerTileAnim(AnimTile):
    def __init__(self, gridPos, spritesheet, collision, animRow, NoOfFrames, timePeriod, damageValue, cost = 1):
        super().__init__(gridPos, spritesheet, collision, animRow, NoOfFrames, timePeriod, cost)
        self.damageValue = damageValue
#Obselete due to random map generation
class TransportTile(Tile):
    def __init__(self, gridPos, sprite, collision, destination):
        super().__init__(gridPos, sprite, collision)
        self.destination = destination
#Idk if this needs to be a thing but sure
class LevelTile(Tile):
    def __init__(self, gridPos, sprite, collision):
        super().__init__(gridPos, sprite, collision)