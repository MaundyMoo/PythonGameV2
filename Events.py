#Class to allow custom input mappings
import pygame, xml.etree.ElementTree as ET
import sys, os, Main
from PyQt4 import QtCore, QtGui, uic
#Could create a PyQt application to edit controls rather than try a clunky pygame interface.
class KeyBinder:
    def __init__(self):
        self.path = Main.getPath('controls.xml')
        self.KeyBinds = ET.parse(self.path)
        self.root = self.KeyBinds.getroot()
        self.setBinds()
    def setBinds(self):
        try:
            self.UP     = eval(self.KeyBinds.find('UP').text)
            self.DOWN   = eval(self.KeyBinds.find('DOWN').text)
            self.LEFT   = eval(self.KeyBinds.find('LEFT').text)
            self.RIGHT  = eval(self.KeyBinds.find('RIGHT').text)
            self.SELECT = eval(self.KeyBinds.find('SELECT').text)
            self.MOVECMND = [self.UP, self.DOWN, self.LEFT, self.RIGHT]
        except TypeError:
            self.UP     = (self.KeyBinds.find('UP').text)
            self.DOWN   = (self.KeyBinds.find('DOWN').text)
            self.LEFT   = (self.KeyBinds.find('LEFT').text)
            self.RIGHT  = (self.KeyBinds.find('RIGHT').text)
            self.SELECT = (self.KeyBinds.find('SELECT').text)
            self.MOVECMND = [self.UP, self.DOWN, self.LEFT, self.RIGHT]
    def Rebind(self, dir: str):
        unbindableEvents = [pygame.MOUSEMOTION, pygame.KEYUP, pygame.ACTIVEEVENT]
        pygame.event.set_blocked(unbindableEvents)
        keys = []
        for i in range(2):
            #pygame.event.clear
            pygame.event.clear()
            keys.append(pygame.event.wait())
        pygame.event.set_allowed(unbindableEvents)
        keys = (keys[0].key, keys[1].key)
        self.root.find(dir).text = str(keys)
        self.KeyBinds.write(self.path)
        self.setBinds()
        #self.KeyBinds.find(dir)
path = Main.getPath("res/UI/Settings.ui") 
settingsUI = uic.loadUiType(path)[0]
class Settings(QtGui.QMainWindow, settingsUI):
    def __init__(self, parent=None):
        #Connects to window
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.path = Main.getPath('controls.xml')
        self.KeyBinds = ET.parse(self.path).getroot()
        self.readControls()
    def readControls(self):
        #This is horrible but I can't think of another way of rewriting this for now because Im terrible
        controlsUP, controlsDOWN, controlsLEFT, controlsRIGHT, controlsSELECT = [], [], [], [], []
        for each in eval(self.KeyBinds.find('UP').text):
            controlsUP.append(pygame.key.name(each))
        for each in eval(self.KeyBinds.find('DOWN').text):
            controlsDOWN.append(pygame.key.name(each))
        for each in eval(self.KeyBinds.find('LEFT').text):
            controlsLEFT.append(pygame.key.name(each))
        for each in eval(self.KeyBinds.find('RIGHT').text):
            controlsRIGHT.append(pygame.key.name(each))
        for each in eval(self.KeyBinds.find('SELECT').text):
            controlsSELECT.append(pygame.key.name(each))
        self.ControlsUP_BindingLabel.setText(str(controlsUP).strip("[]").upper())
        self.ControlsDOWN_BindingLabel.setText(str(controlsDOWN).strip('[]').upper())
        self.ControlsLEFT_BindingLabel.setText(str(controlsLEFT).strip('[]').upper())
        self.ControlsRIGHT_BindingLabel.setText(str(controlsRIGHT).strip('[]').upper())
        self.ControlsSELECT_BindingLabel.setText(str(controlsSELECT).strip('[]').upper())
#Driver for instantiating the Settings Class
def settingsWindow():
    app = QtGui.QApplication(sys.argv)
    ui = Settings(None)
    ui.show()
    app.exec_()