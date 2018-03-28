import pygame, image, Entities, Mapper, Tiles, Events, Main
class SceneBase:
    def __init__(self, width, height):
        self.next = self
        self.width, self.height = width, height
        self.KeyListener = Events.KeyListener()
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
        self.exit = self.font.render("Exit", True, (0, 255, 128))
        self.toRender.extend([self.title, self.start, self.exit])
        self.option = 0
        self.msg = "Start"
        super().__init__(width, height)

    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key in self.KeyListener.SELECT:
                    if self.option == 0:
                        self.msg = "Loading..."
                        self.SwitchToScene(GameScene(self.width, self.height, "res\map.png"))
                    if self.option == 1:
                        self.Terminate()
                elif event.key in self.KeyListener.DOWN:
                    self.option = 1
                elif event.key in self.KeyListener.UP:
                    self.option = 0
    def Update(self):
        if self.option == 0:
            self.toRender[1] = self.font.render(self.msg, True, (0, 255, 255))
            self.toRender[2] = self.font.render("Exit", True, (50, 50, 50))
        elif self.option == 1:
            self.toRender[1] = self.font.render(self.msg, True, (50, 50, 50))
            self.toRender[2] = self.font.render("Exit", True, (0, 255, 255))
    def Render(self, screen):
        screen.fill((255, 0, 0))
        for i in range(0,len(self.toRender)):
            screen.blit(self.toRender[i], ((self.width / 2) - (self.title.get_width())/2, self.height / (len(self.toRender)-i) - (self.title.get_height())))
           
class GameScene(SceneBase):
    #When map/tiles are done will need to probably parse a map in here
    def __init__(self, width, height, mapFile):
        super().__init__(width, height)
        self.map = Mapper.Map(mapFile, "res\TileSheet.png", "res\AnimTileSheet.png")
        self.tileMap = self.map.getTileMap()
        self.player = Entities.Player(5,3,"res\playerSheet.png",self.tileMap,3,10)
        self.Entities = [self.player]
        self.animTiles = []
        self.renderedBack = False
        self.CameraX = 0
        self.CameraY = 0
        
    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.player.handleInputs(event)
                if event.key in self.KeyListener.UP:
                    self.player.dir = 1
                    self.player.flip = False
                    self.renderedBack = False
                    if self.player.Move(0,-1, self.CameraX, self.CameraY):
                        self.CameraY += Tiles.TILESIZE
                elif event.key in self.KeyListener.DOWN:
                    self.player.dir = 0
                    self.player.flip = False
                    self.renderedBack = False
                    if self.player.Move(0,+1, self.CameraX, self.CameraY):
                        self.CameraY -= Tiles.TILESIZE
                elif event.key in self.KeyListener.LEFT:
                    self.player.dir = 2
                    self.player.flip = True
                    self.renderedBack = False
                    if self.player.Move(-1,0, self.CameraX, self.CameraY):
                        self.CameraX += Tiles.TILESIZE
                elif event.key in self.KeyListener.RIGHT:
                    self.player.dir = 2
                    self.player.flip = False
                    self.renderedBack = False
                    if self.player.Move(1,0, self.CameraX, self.CameraY):
                        self.CameraX -= Tiles.TILESIZE
            
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
        #Check if need to switch scene
        if self.player.switchLevel:
            self.SwitchToScene(GameScene(self.width, self.height, self.tileMap[self.player.y][self.player.x].destination))
            
    def Render(self, screen):
        if not self.renderedBack: self.backgroundRender(screen); self.renderedBack = True
        for each in self.animTiles:
            self.tileMap[each[1]][each[0]].Render(screen, self.CameraX, self.CameraY)
        for each in self.Entities:
            self.tileMap[each.y][each.x].Render(screen, self.CameraX, self.CameraY)
            each.Render(screen, self.CameraX, self.CameraY)
            
    def backgroundRender(self, screen):
        self.animTiles = []
        for x in range(int(abs(self.CameraX / Tiles.TILESIZE)), int(abs((self.CameraX / Tiles.TILESIZE)) + abs((Main.WIDTH / Tiles.TILESIZE)))):
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
        self.instruct = self.font3.render("Press any key to close the game...", True, (120, 120, 120))
        super().__init__(width, height)

    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.Terminate()
                
    def Update(self):
        pass
    def Render(self, screen):
        screen.fill((0, 0, 0))
        screen.blit(self.msg, ((self.width/2) - (self.msg.get_width())/2, self.height/2 - (self.msg.get_height())))
        screen.blit(self.credit, ((self.width/2) - (self.credit.get_width())/2, self.height/2))
        screen.blit(self.instruct, ((self.width/2) - (self.instruct.get_width())/2, 2*self.height/3 + (self.instruct.get_height())))