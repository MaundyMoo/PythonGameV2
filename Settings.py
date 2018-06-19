import sys, os
from PyQt4 import QtCore, QtGui, uic
dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)
window = uic.loadUiType("res/UI/Settings.ui")[0]
class Settings(QtGui.QMainWindow, window):
    def __init__(self, parent=None):
        #Connects to window
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
app = QtGui.QApplication(sys.argv)
ui = Settings(None)
ui.show()
app.exec_()