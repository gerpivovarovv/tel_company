from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic


class WinReg(QMainWindow):
    def __init__(self):
        super(WinReg, self).__init__()
        uic.loadUi('reg.ui', self)