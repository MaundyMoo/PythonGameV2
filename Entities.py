import Main, Image, pygame, Tiles, Events, Pathing
class Entity:
    def __init__(self, x, y, spritesheet, map, frames, interval, colour = (255,0,0)):
        self.x, self.y, self.map = x, y, map
        
        #Sprite / Animation initialisation
        self.flip = False
        self.spriteSheet = Image.SpriteSheet(spritesheet, 32)
        spr = self.spriteSheet.returnTile(0, 0)
        self.sprite = self.ImgToSprite(spr)
        #Idk what this is doing here tbh
        self.damageSprite = Image.spriteFlash(spr, colour)
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
        self.maxHealth = 20
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
            if self.y + dY < 0: dY = 0;return False
            if self.x + dX < 0: dX = 0; return False
            #Stops mpving off of the map 
            if self.x + dX >= len(self.map[0]): dX = 0; return False
            if self.y + dY >= len(self.map): dY = 0;return False
            #This allows the player to move past the point where the camera couldn't on the far right / bottom and return to centre of the screen without the camera moving
            if (dX is not 0) and (self.x + dX >= (self.xCentre + (abs(len(self.map[0]) - (Main.WIDTH / Tiles.TILESIZE))))) and (abs(OffsetX) == abs(len(self.map[0]) * Tiles.TILESIZE - Main.WIDTH)): self.x+=dX; return False
            if (dY is not 0) and (self.y + dY >= (self.yCentre + (abs(len(self.map) - (Main.HEIGHT / Tiles.TILESIZE))))) and (abs(OffsetY) == abs(len(self.map) * Tiles.TILESIZE - Main.HEIGHT)): self.y+=dY; return False
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
    #This is called when the player initiates an attack on an enemy by walking into them
    def Combat(self, enemy):
        enemy.TurnCombat = True
        if enemy.health < self.Damage:
            enemy.die()
        else:
            self.health -= enemy.Damage
            enemy.health -= self.Damage
        #Display some visual feedback from battle, maybe print to console if need be as a form of combat log, but Id rather not
        #Maybe a floating combat text kind of thing, like WoW but 2D, although may be difficult
        #As long as there's some audiovisual feedback to the player
    #This is called when a player gets attacked by an enemy without the player doing any attack
    def Attacked(self, enemy):   
        enemy.TurnCombat = True
        self.health -= enemy.Damage
    def die(self):
        self.isDead = True

    def getX(self):
        return self.x
    def getY(self): 
        return self.y
        
class Enemy(Entity):
    def __init__(self, x, y, spritesheet, map, frames, interval, animRow, agrorange):
        super().__init__(x, y, spritesheet, map, frames, interval)
        self.maxHealth = self.health = self.Damage= 0
        self.isDead = False
        self.agrorange = agrorange
        #Stops the combat and Attacked methods being called both in one turn
        self.TurnCombat = False
        
    def Update(self):
        super().Update()
        if self.health <= 0:
            self.die()
    def inRange(self, player):
        distanceToPlayer = ((self.x - player.x)**2 + (self.y - player.y)**2)**0.5
        if distanceToPlayer < self.agrorange:
            return True
        else:
            return False
    def move(self, graph, player, entities, tileMap):
        if self.inRange(player):
            path = graph.Astar([self.y, self.x], [player.y, player.x])
            playerCoords, nextCoords = tuple([player.x, player.y]), tuple([path[0][1], path[0][0]])
            willMove = True
            for each in entities:
                if nextCoords == (each.x, each.y):
                    willMove = False
                    break
            if not nextCoords == playerCoords and willMove:
                self.x = path[0][1]
                self.y = path[0][0]
                if type(tileMap[self.y][self.x]) == Tiles.DangerTileAnim:
                    self.health -= tileMap[self.y][self.x].damageValue
            elif nextCoords == playerCoords and not self.TurnCombat:
                player.Attacked(self)
            self.TurnCombat = False
        else:
            pass
    def die(self):
        self.isDead = True
#might do multiple classes, one for each enemy type
class TestEnemy(Enemy):
    def __init__(self, x, y, map, agrorange = 8):
        #Entity Constants
        path = Main.getPath("res/EnemySheet.png")
        spritesheet = path; frames = 1; interval = 20; animRow = 0
        super().__init__(x, y, spritesheet, map, frames, interval, animRow, agrorange)
        #Stats
        self.maxHealth = self.health = 5
        self.Damage = 1