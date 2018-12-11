'''
This class is responsable for the majority of the UI elements that
pertain to player information
'''
import pygame
class Logger:
    def __init__(self, pos: int, width: int, height: int):
        self.log = []
        #Corner position?
        #I don't know if it's worth having these as attributes rather than reading from a constants file
        self.position = pos
        self.width, self.height = width, height
        self.logAmount = 20
        self.textOffset = 5
        #Initialise attributes with a default value (0 or null crashes unfortunately)
        self.playerMaxHealth: int = 1
        self.playerHealth: int = 1

        self.Font = pygame.font.SysFont("Impact", 20)
        self.healthX = 10
        self.healthBarWidth = self.width - self.healthX * 2
        self.healthBarHeight = 20
        self.healthY = self.height - self.healthBarHeight * 2
        self.healthOffset = 10

    #How do I actually want to log events, parse the string in or parse the action and let the method handle creating a string
    def logDeath(self, entity: str):
        msg = entity + ' was killed.'
        pygMsg = self.Font.render(msg, True, (0, 0, 0))
        self.log.append(pygMsg)
    def logCombat(self, Attacker: str, Defender: str, damage: int):
        msg = Attacker + ' hit ' + Defender + ' for ' + str(damage) + '.'
        pygMsg = self.Font.render(msg, True, (0,0,0))
        self.log.append(pygMsg)
    def logDamage(self, player: str, Damage: int):
        msg = player + ' took ' + str(Damage) + ' damage.'
        pygMsg = self.Font.render(msg, True, (0, 0, 0))
        self.log.append(pygMsg)
    def Update(self, playerHealth: int, playerMaxHealth: int):
        '''
        The question is,
        Do I need to actually update attributes here,
        or simply draw them to the screen
        Need to update the current values of playerHealth etc.
        '''
        self.playerHealth = playerHealth
        self.playerMaxHealth = playerMaxHealth
        while len(self.log) > self.logAmount:
            self.log.pop(0)
    def Render(self, screen):
        '''
        Should probably have a way of anchoring elements native to the logger
        onto the object, so the position of rendering log text is relative to
        the logger's position on the screen, rather than relative to the screen
        itself.
        oh god it's css all over again /o\
        Just offset all X positions by self.position, the height has no offset so it doesn't matter
        '''
        #draw.rect(screen, (r,g,b), (posX, posY, width, height))
        pygame.draw.rect(screen, (100,100,100), (self.position, 0, self.width, self.height))
        pygame.draw.rect(screen, (0, 0, 0), (self.position, self.Font.get_height() * self.logAmount + self.textOffset, self.width, 4))
        # Draws three rectangles for the health bar, Health bar in green, back in red, and border in black
        # Border
        pygame.draw.rect(screen, (0, 0, 0), (self.position + self.healthX - self.healthOffset / 2, self.healthY - self.healthOffset / 2, self.healthBarWidth + self.healthOffset, self.healthBarHeight + self.healthOffset))
        # Damage
        pygame.draw.rect(screen, (255, 0, 0), (self.position + self.healthX, self.healthY, self.healthBarWidth, self.healthBarHeight))
        # Health
        pygame.draw.rect(screen, (0, 255, 0), (self.position + self.healthX, self.healthY, self.healthBarWidth * (self.playerHealth / self.playerMaxHealth), self.healthBarHeight))
        # Text
        healthText = self.Font.render((str(self.playerHealth) + "/" + str(self.playerMaxHealth)), True, (0, 0, 100))
        screen.blit(healthText, (self.position + self.healthX + self.healthBarWidth / 2 - healthText.get_width() / 2, self.healthY - self.healthOffset / 4))

        #Log
        for i in range(0, len(self.log)):
            screen.blit(self.log[i], (self.position + 5, self.Font.get_height() * i + self.textOffset))