import Image, pygame, Main
tileSize = TILESIZE = 64
class Tile:
    #Tiles will always be square
    TILESIZE = tileSize
    def __init__(self, gridPos, sprite, collision):
        #Pygame cannot natively read PIL png formats, so have to convert to string to let pygame read it
        self.sprite = pygame.image.fromstring(sprite.tobytes(), sprite.size, sprite.mode)
        self.sprite = pygame.transform.scale(self.sprite, (self.TILESIZE, self.TILESIZE))
        #Boolean flags
        self.collision = collision  

        self.pos = gridPos
    def Render(self, screen, OffsetX, OffsetY):
        screen.blit(self.sprite, ((self.pos[0] * self.TILESIZE) + OffsetX, (self.pos[1] * self.TILESIZE) + OffsetY))
    def Update(self):
        pass
    def isCollidable(self):
        return self.collision
    
class AnimTile(Tile):
    def __init__(self, gridPos, spritesheet,collision, animRow, NoOfFrames, timePeriod):
        self.NoOfFrames = NoOfFrames
        self.timePeriod = timePeriod
        self.spriteSheet = spritesheet
        self.animRow = animRow
        #Tile needs an initial sprite to set the attribute sprite
        initialSprite = self.spriteSheet.returnTile(0, self.animRow)
        super().__init__(gridPos, initialSprite, collision)
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
    def __init__(self, gridPos, spritesheet, collision, animRow, NoOfFrames, timePeriod, damageValue):
        super().__init__(gridPos, spritesheet, collision, animRow, NoOfFrames, timePeriod)
        self.damageValue = damageValue
        
class TransportTile(Tile):
    def __init__(self, gridPos, sprite, collision, destination):
        super().__init__(gridPos, sprite, collision)
        self.destination = destination