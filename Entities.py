import Main, Image, pygame, Tiles, Events
class Entity:
    def __init__(self, x, y, spritesheet, map, frames, interval):
        self.x, self.y, self.map = x, y, map
        
        #Sprite / Animation initialisation
        self.flip = False
        self.spriteSheet = Image.SpriteSheet(spritesheet, 32)
        self.sprite = self.ImgToSprite(self.spriteSheet.returnTile(0, 0))
        self.sprite = pygame.transform.scale(self.sprite, (Tiles.TILESIZE, Tiles.TILESIZE))
        
        self.frames = frames
        self.interval = interval
        self.animRow = 0
        self.tick = 0
    def ImgToSprite(self, spr):
        Sprite = pygame.image.fromstring(spr.tobytes(), spr.size, spr.mode)
        Sprite = pygame.transform.scale(Sprite, (Tiles.TILESIZE, Tiles.TILESIZE))
        Sprite = pygame.transform.flip(Sprite, self.flip, False)
        return Sprite
    def Update(self):
        self.animate()
    def Render(self, screen, OffsetX, OffsetY):
        screen.blit(self.sprite,(self.x * Tiles.TILESIZE + OffsetX,self.y * Tiles.TILESIZE + OffsetY))
    def Move(self):
        pass
    def die(self):
        pass
    def animate(self):
        self.tick += 1 
        animTime = (self.frames + 1) * self.interval - 1
        if self.tick > animTime:
            self.tick = 0
        self.sprite = self.ImgToSprite(self.spriteSheet.returnTile(self.tick // self.interval, self.animRow))
        
class Player(Entity):
    def __init__(self, x, y, spritesheet, map, frames, interval):
        super().__init__(x, y, spritesheet, map, frames, interval)
        #Camera / Map constants
        self.xCentre = int((Main.WIDTH / Tiles.TILESIZE) / 2)
        self.yCentre = int((Main.HEIGHT / Tiles.TILESIZE) / 2)

        #Health
        self.isDead = False
        self.maxHealth = 5
        self.health = self.maxHealth
        #Health bar drawing
        self.healthBarHeight = 20
        self.healthBarWidth = 150
        self.healthX = self.healthY = 10
        self.healthOffset = 10
        self.healthFont = pygame.font.SysFont("Impact", 20)
        self.switchLevel = False
        #Combat Stats
        self.Damage = 3
    def Render(self, screen, OffsetX, OffsetY):
        super().Render(screen, OffsetX, OffsetY)
        #Draws three rectangles for the health bar, Health bar in green, back in red, and border in black
        #Border
        pygame.draw.rect(screen, (0,0,0), (self.healthX - self.healthOffset/2, self.healthY - self.healthOffset/2, self.healthBarWidth + self.healthOffset, self.healthBarHeight + self.healthOffset))
        #Damage
        pygame.draw.rect(screen, (255,0,0), (self.healthX, self.healthY, self.healthBarWidth, self.healthBarHeight))
        #Health
        pygame.draw.rect(screen, (0,255,0), (self.healthX, self.healthY, self.healthBarWidth * (self.health / self.maxHealth), self.healthBarHeight))
        #Text
        healthText = self.healthFont.render((str(self.health) + "/" + str(self.maxHealth)), True,(0,0,100)) 
        screen.blit(healthText, (self.healthX + self.healthBarWidth/2 - healthText.get_width()/2, self.healthY - self.healthOffset/4))
    def Update(self):
        if self.health <= 0:
            self.die()
        super().Update()

    def Move(self, dX, dY, OffsetX, OffsetY, entities):
        #If the tile being moved onto has an event, trigger it
        try:
            if self.x + dX not in range(0, len(self.map[0])): dX = 0
            if self.y + dY not in range(0, len(self.map)): dY = 0
            if type(self.map[self.y + dY][self.x + dX]) == Tiles.DangerTileAnim:
                self.health -= self.map[self.y + dY][self.x + dX].damageValue 
            elif type(self.map[self.y + dY][self.x + dX]) == Tiles.TransportTile:
                self.switchLevel = True
        except IndexError:
            pass
        #Returns True or false depending on whether it wants the camera to move with the character or not
        #Try-except is used to stop the player from moving off the screen out of bounds
        try:
            #collision check
            if self.map[self.y+dY][self.x+dX].isCollidable(): return False
            for each in entities[1::]:
                if (self.x + dX) == each.x and (self.y + dY) == each.y: 
                    if issubclass(type(each), Enemy):
                        self.Combat(each)
                        return False
                    else:
                        print("Oopsies I made an error")
            #This stops the player moving off the screen to the left / top
            if self.y + dY < 0: dY = 0; return False
            if self.x + dX < 0: dX = 0; return False
            #Stops mpving off of the map 
            if self.x + dX > len(self.map): dX = 0; return False
            if self.y + dY > len(self.map[0]): dY = 0; return False
            #This allows the player to move past the point where the camera couldn't on the far right / bottom and return to centre of the screen without the camera moving
            if (dX is not 0) and (self.x + dX >= (self.xCentre + (abs(len(self.map[0]) - (Main.WIDTH / Tiles.TILESIZE))))) and (abs(OffsetX) == abs(len(self.map[0]) * Tiles.TILESIZE - Main.WIDTH)): self.x+=dX; return False
            if (dY is not 0) and (self.y + dY >= (self.yCentre + (abs(len(self.map[1]) - (Main.HEIGHT / Tiles.TILESIZE))))) and (abs(OffsetY) == abs(len(self.map[1]) * Tiles.TILESIZE - Main.HEIGHT)): self.y+=dY; return False
            #This allows the player to move at the top and left without needing the camera to follow (as it would go out of bounds)
            if dX is not 0 and self.x + dX <= self.xCentre and OffsetX == 0: self.x += dX;return False
            if dY is not 0 and self.y + dY <= self.yCentre and OffsetY == 0: self.y += dY;return False
            self.x += dX
            self.y += dY
            return True
        except IndexError:
            return False
    def handleInputs(self, input):
        pass
    def Combat(self, enemy):
        if enemy.health < self.Damage:
            enemy.die()
        else:
            self.health -= enemy.Damage
            enemy.health -= self.Damage
        #Display some visual feedback from battle, maybe print to console if need be as a form of combat log, but Id rather not
        #Maybe a floating combat text kind of thing, like WoW but 2D, although may be difficult
        #As long as there's some audiovisual feedback to the player
        
    def die(self):
        self.isDead = True

class Enemy(Entity):
    def __init__(self, x, y, spritesheet, map, frames, interval, animRow):
        super().__init__(x, y, spritesheet, map, frames, interval)
        self.maxHealth = self.health = self.Damage= 0
        self.isDead = False
        
    def Update(self):
        super().Update()
        if self.health <= 0:
            self.die()
            
    def move(self, playerX, playerY, entities):
        #Currently just runs straight towards the player, checking only the tiles around it, need to replace with an actual path finding algorithm, e.g. A*
        dY, dX = 0, 0
        #check y
        if playerY > self.y:
            dY = 1
        elif playerY < self.y:
            dY = -1
        if self.map[self.y + dY][self.x].collision == True:
            dY = 0
        else:
            for each in entities:
                if (self.y + dY, self.x) == (each.y, each.x):
                    dY = 0
                    break
        #check x
        if dY == 0 or playerY == self.y:
            if playerX > self.x:
                dX = 1
            elif playerX < self.x:
                dX = -1
            if self.map[self.y][self.x + dX].collision == True:
                dX = 0
            else:
                for each in entities:
                    if (self.y, self.x + dX) == (each.y, each.x):
                        dX = 0
                        break   
        self.y += dY; self.x += dX
        if type(self.map[self.y][self.x]) == Tiles.DangerTileAnim:
            self.health -= self.map[self.y][self.x].damageValue
            
    def die(self):
        self.isDead = True
#might do multiple classes, one for each enemy type
class TestEnemy(Enemy):
    def __init__(self, x, y, map):
        #Entity Constants
        spritesheet = "res\EnemySheet.png"; frames = 1; interval = 20; animRow = 0
        super().__init__(x, y, spritesheet, map, frames, interval, animRow)
        #Stats
        self.maxHealth = self.health = 5
        self.Damage = 1