#Class to allow custom input mappings
import pygame, xml.etree.ElementTree as ET
class KeyListener:
    def __init__(self):
        self.KeyBinds = ET.parse('controls.xml').getroot()
        self.UP     = eval(self.KeyBinds.find('UP').text)
        self.DOWN   = eval(self.KeyBinds.find('DOWN').text)
        self.LEFT   = eval(self.KeyBinds.find('LEFT').text)
        self.RIGHT  = eval(self.KeyBinds.find('RIGHT').text)
        self.SELECT = eval(self.KeyBinds.find('SELECT').text)
    #Probably dont need a class to do this (when am I ever going to initialise this more than once)