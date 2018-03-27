import Main, Image, pygame, Tiles, Events
class Entity:
    def __init__(self, x, y, map):
        self.x, self.y, self.sprite, self.map = x, y, None, map
        self.flip = False
    def ImgToSprite(self, spr):
        Sprite = pygame.image.fromstring(spr.tobytes(), spr.size, spr.mode)
        Sprite = pygame.transform.scale(Sprite, (Tiles.TILESIZE, Tiles.TILESIZE))
        Sprite = pygame.transform.flip(Sprite, self.flip, False)
        return Sprite
    def Update(self):
        pass
    def Render(self, screen, OffsetX, OffsetY):
        screen.blit(self.sprite,(self.x * Tiles.TILESIZE + OffsetX,self.y * Tiles.TILESIZE + OffsetY))
    def Move(self):
        pass
    def die(self):
        pass
        
class Player(Entity):
    def __init__(self, x, y, spritesheet, map, frames, interval):
        super().__init__(x, y,map)
        #Camera / Map constants
        self.xCentre = int((Main.WIDTH / Tiles.TILESIZE) / 2)
        self.yCentre = int((Main.HEIGHT / Tiles.TILESIZE) / 2)
        #Sprite / Animation initialisation
        self.spriteSheet = Image.SpriteSheet(spritesheet, 32)
        self.sprite = self.ImgToSprite(self.spriteSheet.returnTile(0, 0))
        self.sprite = pygame.transform.scale(self.sprite, (Tiles.TILESIZE, Tiles.TILESIZE))
        self.frames = frames
        self.interval = interval
        self.dir = 0
        self.tick = 0
        #Game variable initialisation
        self.isDead = False
        self.maxHealth = 100
        self.health = self.maxHealth
        self.healthBarHeight = 20
        self.healthBarWidth = 150
        self.healthX = self.healthY = 10
        self.healthOffset = 10
    def Render(self, screen, OffsetX, OffsetY):
        super().Render(screen, OffsetX, OffsetY)
        #Draws three rectangles for the health bar, Health bar in green, back in red, and border in black
        pygame.draw.rect(screen, (0,0,0), (self.healthX - self.healthOffset/2, self.healthY - self.healthOffset/2, self.healthBarWidth + self.healthOffset, self.healthBarHeight + self.healthOffset))
        pygame.draw.rect(screen, (255,0,0), (self.healthX, self.healthY, self.healthBarWidth, self.healthBarHeight))
        pygame.draw.rect(screen, (0,255,0), (self.healthX, self.healthY, self.healthBarWidth * (self.health / self.maxHealth), self.healthBarHeight))
    def Update(self):
        if type(self.map[self.y][self.x]) == Tiles.DangerTileAnim:
            self.health -= self.map[self.y][self.x].damageValue 
        if self.health <= 0:
            #me_irl
            self.die()
        self.animate()
    def animate(self):
        self.tick += 1 
        animTime = (self.frames + 1) * self.interval - 1
        if self.tick > animTime:
            self.tick = 0
        self.sprite = self.ImgToSprite(self.spriteSheet.returnTile(self.tick // self.interval, self.dir))

    def Move(self, dX, dY, OffsetX, OffsetY):
        #Returns True or false depending on whether it wants the camera to move with the character or not
        #Try-except is used to stop the player from moving off the screen out of bounds
        try:
            #collision check
            if self.map[self.y+dY][self.x+dX].isCollidable(): return False; 
            #This stops the player moving off the screen to the left / top
            if self.y + dY < 0: dY = 0; return False;
            if self.x + dX < 0: dX = 0; return False;
            #Stops mpving off of the map 
            if self.x + dX > len(self.map): dX = 0; return False;
            if self.y + dY > len(self.map[0]): dY = 0; return False;
            #This allows the player to move past the point where the camera couldn't on the far right / bottom and return to centre of the screen without the camera moving
            if (dX is not 0) and (self.x + dX >= (self.xCentre + (abs(len(self.map[0]) - (Main.WIDTH / Tiles.TILESIZE))))) and (abs(OffsetX) == abs(len(self.map[0]) * Tiles.TILESIZE - Main.WIDTH)): self.x+=dX; return False;
            if (dY is not 0) and (self.y + dY >= (self.yCentre + (abs(len(self.map[1]) - (Main.HEIGHT / Tiles.TILESIZE))))) and (abs(OffsetY) == abs(len(self.map[1]) * Tiles.TILESIZE - Main.HEIGHT)): self.y+=dY; return False;
            #This allows the player to move at the top and left without needing the camera to follow (as it would go out of bounds)
            if dX is not 0 and self.x + dX <= self.xCentre and OffsetX == 0: self.x += dX;return False;
            if dY is not 0 and self.y + dY <= self.yCentre and OffsetY == 0: self.y += dY;return False; 
            self.x += dX
            self.y += dY
            return True
        except IndexError:
            return False
    def handleInputs(self, input):
        pass
    #me_irl
    def die(self):
        self.isDead = True