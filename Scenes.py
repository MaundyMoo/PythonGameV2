import pygame, image, Entities, Mapper, Tiles, Events, Main
class SceneBase:
    def __init__(self, width, height):
        self.next = self
        self.width, self.height = width, height
        self.KeyBinder = Events.KeyBinder()
    def ProcessInput(self, events, pressed_keys):
        print("ProcessInput not overwritten")
    def Update(self):
        print("Update not overwritten")
    def initialRender(self, screen):
        print("initialRender not overwritten")
    def Render(self, screen):
        print("Render not overwritten")
    def SwitchToScene(self, next_scene):
        self.next = next_scene
    def Terminate(self):
        self.SwitchToScene(None)
        pygame.quit()

class TitleScene(SceneBase):
    font = None 
    title = None
    def __init__(self, width, height):
        self.font = pygame.font.SysFont("arial", 64)
        self.toRender = []
        self.title = self.font.render("QWERTY", True, (50, 255, 128))
        self.start = self.font.render("Start", True, (0, 255, 128))
        self.settings = self.font.render("Settings", True, (0, 255, 128))
        self.exit = self.font.render("Exit", True, (0, 255, 128))
        self.toRender.extend([self.title, self.start, self.settings, self.exit])
        self.option = 0
        self.msg = "Start"
        super().__init__(width, height)

    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key in self.KeyBinder.SELECT:
                    #Start
                    if self.option == 0:
                        self.SwitchToScene(LoadingScene(self.width, self.height))
                    #Settings
                    elif self.option == 1:
                        #need to stop multiple windows being after the first one is closed
                        Events.settingsWindow()
                        self.SwitchToScene(SettingsScene(self.width, self.height))
                    #Exit
                    elif self.option == 2:
                        self.Terminate()
                elif event.key in self.KeyBinder.DOWN:
                    self.option += 1
                elif event.key in self.KeyBinder.UP:
                    self.option -= 1
                if self.option < 0: self.option = 0
                if self.option > 2: self.option = 2
    def Update(self):
        if self.option == 0:
            self.toRender[1] = self.font.render(self.msg, True, (0, 255, 255))
            self.toRender[2] = self.font.render("Settings", True, (50, 50, 50))
            self.toRender[3] = self.font.render("Exit", True, (50, 50, 50))
        elif self.option == 1:
            self.toRender[1] = self.font.render(self.msg, True, (50, 50, 50))
            self.toRender[2] = self.font.render("Settings", True, (0, 255, 255))
            self.toRender[3] = self.font.render("Exit", True, (50, 50, 50))
        elif self.option == 2:
            self.toRender[1] = self.font.render(self.msg, True, (50, 50, 50))
            self.toRender[2] = self.font.render("Settings", True, (50, 50, 50))
            self.toRender[3] = self.font.render("Exit", True, (0, 255, 255))
    def Render(self, screen):
        screen.fill((255, 0, 0))
        for i in range(0,len(self.toRender)):
            screen.blit(self.toRender[i], ((self.width / 2) - (self.title.get_width())/2, self.toRender[i].get_height()*i))

class LoadingScene(SceneBase):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.font = pygame.font.SysFont("arial", 64)
        self.msg = self.font.render("Loading", True, (0, 0, 255))
        self.hasRendered = False
    def Update(self):
        if self.hasRendered:
            self.SwitchToScene(GameScene(self.width, self.height, "res\map.png"))
    def ProcessInput(self, events, pressed_keys):
        pass
    def Render(self, screen):
        screen.fill((128, 128, 255))
        screen.blit(self.msg, ((int(self.width / 2)) - int(self.msg.get_width()/2), int(self.height/2)-int(self.msg.get_height()/2)))
        self.hasRendered = True
        
#May have to abandon PyQt for controls although Idk
class SettingsScene(SceneBase):
    def __init__(self, width, height):
        self.option = 0
        super().__init__(width, height)
    def ProcessInput(self, events, pressed_keys):
        pass
    def Update(self):
        pass
    def Render(self, screen):
        screen.fill((128, 128, 255))
           
class GameScene(SceneBase):
    #When map/tiles are done will need to probably parse a map in here
    def __init__(self, width, height, mapFile):
        super().__init__(width, height)
        self.map = Mapper.Map(mapFile, "res\TileSheet.png", "res\AnimTileSheet.png")
        self.tileMap = self.map.getTileMap()
        self.player = Entities.Player(2,2,"res\playerSheet.png",self.tileMap,3,10)
        #Will need to make a system of entity placement that isn't hard coded, but Im not entirely sure how other than random generation or messing around with alpha channels.
        self.DummyEnemies = [Entities.TestEnemy(5,5,self.tileMap),
                             Entities.TestEnemy(5,7,self.tileMap),
                             Entities.TestEnemy(4,6,self.tileMap),
                             Entities.TestEnemy(6,6,self.tileMap)]
        self.Entities = [self.player]
        self.Entities.extend(self.DummyEnemies)
        self.animTiles = []
        self.renderedBack = False
        self.CameraX = 0
        self.CameraY = 0
        
    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.player.handleInputs(event)
                if event.key in self.KeyBinder.UP:
                    self.player.animRow = 1
                    self.player.flip = False
                    self.renderedBack = False
                    if self.player.Move(0,-1, self.CameraX, self.CameraY, self.Entities):
                        self.CameraY += Tiles.TILESIZE
                elif event.key in self.KeyBinder.DOWN:
                    self.player.animRow = 0
                    self.player.flip = False
                    self.renderedBack = False
                    if self.player.Move(0,+1, self.CameraX, self.CameraY, self.Entities):
                        self.CameraY -= Tiles.TILESIZE
                elif event.key in self.KeyBinder.LEFT:
                    self.player.animRow = 2
                    self.player.flip = True
                    self.renderedBack = False
                    if self.player.Move(-1,0, self.CameraX, self.CameraY, self.Entities):
                        self.CameraX += Tiles.TILESIZE
                elif event.key in self.KeyBinder.RIGHT:
                    self.player.animRow = 2
                    self.player.flip = False
                    self.renderedBack = False
                    if self.player.Move(1,0, self.CameraX, self.CameraY, self.Entities):
                        self.CameraX -= Tiles.TILESIZE
                for commands in self.KeyBinder.MOVECMND:
                    if event.key in commands:
                        for each in self.Entities[1::]:
                            each.move(self.player, self.Entities[1::])
            
    def Update(self):
    #Top left is (0,0) so offset is done in negative
        #Prevents the camera going off of the RightMost boundary 
        if self.CameraX < -(self.map.getWidth() * Tiles.TILESIZE - Main.WIDTH):
            self.CameraX = -(self.map.getWidth() * Tiles.TILESIZE - Main.WIDTH)
        #Stops Left most boundary
        elif self.CameraX > 0:
            self.CameraX = 0
        #Stops bottom most boundary
        if self.CameraY < -(self.map.getHeight() * Tiles.TILESIZE - Main.HEIGHT):
            self.CameraY = -(self.map.getHeight() * Tiles.TILESIZE - Main.HEIGHT)
        #Stops upper most boundary
        elif self.CameraY > 0:
            self.CameraY = 0
        #Updates every entity
        for each in self.Entities:
            each.Update()
        #Checks if Player be dead
        if self.player.isDead:
            self.SwitchToScene(EndScene(self.width, self.height))
        for each in self.Entities[1::]:
            if each.isDead:
                self.Entities.remove(each)
        #Check if need to switch scene
        if self.player.switchLevel:
            self.SwitchToScene(GameScene(self.width, self.height, self.tileMap[self.player.y][self.player.x].destination))
            
    def Render(self, screen):
        if not self.renderedBack: self.backgroundRender(screen); self.renderedBack = True
        for each in self.animTiles:
            self.tileMap[each[1]][each[0]].Render(screen, self.CameraX, self.CameraY)
        for each in self.Entities[1::]:
            self.tileMap[each.y][each.x].Render(screen, self.CameraX, self.CameraY)
            each.Render(screen, self.CameraX, self.CameraY)
        self.tileMap[self.player.y][self.player.x].Render(screen, self.CameraX, self.CameraY)
        self.player.Render(screen, self.CameraX, self.CameraY)
    
    #Used to redraw the tiles in the background after the player character moves
    def backgroundRender(self, screen):
        self.animTiles = []
        for x in range(int(abs(self.CameraX / Tiles.TILESIZE)), int(abs(self.CameraX / Tiles.TILESIZE) + abs(Main.WIDTH / Tiles.TILESIZE))):
            for y in range(int(abs(self.CameraY / Tiles.TILESIZE)), int(abs((self.CameraY / Tiles.TILESIZE)) + abs((Main.HEIGHT / Tiles.TILESIZE)))):
                self.tileMap[y][x].Render(screen, self.CameraX, self.CameraY)
                if type(self.tileMap[y][x]) == Tiles.AnimTile or issubclass(type(self.tileMap[y][x]), Tiles.AnimTile):
                    self.animTiles.append((x,y))

class EndScene(SceneBase):
    def __init__(self, width, height):
        self.font = pygame.font.SysFont("Impact", 128)
        self.font2 = pygame.font.SysFont("arial", 48)
        self.font3 = pygame.font.SysFont("arial", 24)
        
        self.msg = self.font.render("You died", True, (255, 0, 0))
        self.credit = self.font2.render("Game Made By Maund", True, (0, 255, 128))
        self.instruct = self.font3.render("Press return to close the game...", True, (120, 120, 120))
        super().__init__(width, height)

    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key in self.KeyBinder.SELECT:
                    self.Terminate()
                
    def Update(self):
        pass
    def Render(self, screen):
        screen.fill((0, 0, 0))
        screen.blit(self.msg, ((self.width/2) - (self.msg.get_width())/2, self.height/2 - (self.msg.get_height())))
        screen.blit(self.credit, ((self.width/2) - (self.credit.get_width())/2, self.height/2))
        screen.blit(self.instruct, ((self.width/2) - (self.instruct.get_width())/2, 2*self.height/3 + (self.instruct.get_height())))