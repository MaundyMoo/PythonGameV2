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
    #How do I actually want to log events, parse the string in or parse the action and let the method handle creating a string
    def logEvent(self, text: str):
        pass
    def Update(self, playerHealth: int, playerMaxHealth: int):
        '''
        The question is,
        Do I need to actually update attributes here,
        or simply draw them to the screen
        '''
        pass
    def Render(self, screen):
        '''
        Should probably have a way of anchoring elements native to the logger
        onto the object, so the position of rendering log text is relative to
        the logger's position on the screen, rather than relative to the screen
        itself.
        oh god it's css all over again /o\
        '''
        pygame.draw.rect(screen, (100,100,100), (self.position, 0, self.width, self.height))