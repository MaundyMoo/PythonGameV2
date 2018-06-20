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
settingsUI = uic.loadUiType("res/UI/Settings.ui")[0]
class Settings(QtGui.QMainWindow, settingsUI):
    def __init__(self, parent=None):
        #Connects to window
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.KeyBinds = ET.parse('controls.xml').getroot()
        self.readControls()
        self.ControlsUP_Button.clicked.connect(self.rebindUP)
    def readControls(self):
        self.ControlsUP_BindingLabel.setText(str(eval(self.KeyBinds.find('UP').text)))
        self.ControlsDOWN_BindingLabel.setText(str(eval(self.KeyBinds.find('DOWN').text)))
        self.ControlsLEFT_BindingLabel.setText(str(eval(self.KeyBinds.find('LEFT').text)))
        self.ControlsRIGHT_BindingLabel.setText(str(eval(self.KeyBinds.find('RIGHT').text)))
        self.ControlsSELECT_BindingLabel.setText(str(eval(self.KeyBinds.find('SELECT').text)))
    #Need to learn how to read a single keystroke
    def rebindUP(self):
        pass
    def rebindDOWN(self):
        pass
    def rebindLEFT(self):
        pass
    def rebindRIGHT(self):
        pass
    def rebindSELECT(self):
        pass
#Driver for instantiating the Settings Class
def settingsWindow():
    app = QtGui.QApplication(sys.argv)
    ui = Settings(None)
    ui.show()
    app.exec_()