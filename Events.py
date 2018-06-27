#Class to allow custom input mappings
import pygame, xml.etree.ElementTree as ET
import sys, os
from PyQt4 import QtCore, QtGui, uic
#Could create a PyQt application to edit controls rather than try a clunky pygame interface.
class KeyBinder:
    def __init__(self):
        self.KeyBinds = ET.parse('controls.xml').getroot()
        self.UP     = eval(self.KeyBinds.find('UP').text)
        self.DOWN   = eval(self.KeyBinds.find('DOWN').text)
        self.LEFT   = eval(self.KeyBinds.find('LEFT').text)
        self.RIGHT  = eval(self.KeyBinds.find('RIGHT').text)
        self.SELECT = eval(self.KeyBinds.find('SELECT').text)
        self.MOVECMND = [self.UP, self.DOWN, self.LEFT, self.RIGHT]
    #Probably dont need a class to do this (when am I ever going to initialise this more than once)
WORKING_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(WORKING_DIRECTORY, "res/UI/Settings.ui") 
settingsUI = uic.loadUiType(path)[0]
class Settings(QtGui.QMainWindow, settingsUI):
    def __init__(self, parent=None):
        #Connects to window
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.KeyBinds = ET.parse('controls.xml').getroot()
        self.readControls()
        self.ControlsUP_Button.clicked.connect(self.rebindUP)
        self.ControlsDOWN_Button.clicked.connect(self.rebindDOWN)
        self.ControlsLEFT_Button.clicked.connect(self.rebindLEFT)
        self.ControlsRIGHT_Button.clicked.connect(self.rebindRIGHT)
        self.ControlsSELECT_Button.clicked.connect(self.rebindSELECT)
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
    #Need to learn how to read a single keystroke
    def rebindUP(self):
        print("Rebind Up")
        #Pygame events only work when in focus, but QtEvent uses different codes for each character, presumably the ASCII / unicode value
        pygame.event.clear()
        pygame.event.wait()
        print(pygame.event.get())
    def rebindDOWN(self):
        print("Rebind Down")
    def rebindLEFT(self):
        print("Rebind Left")
    def rebindRIGHT(self):
        print("Rebind Right")
    def rebindSELECT(self):
        print("Rebind Select")
#Driver for instantiating the Settings Class
def settingsWindow():
    app = QtGui.QApplication(sys.argv)
    ui = Settings(None)
    ui.show()
    app.exec_()