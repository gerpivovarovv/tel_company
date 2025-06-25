from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic


class FirstWin(QMainWindow):
    def __init__(self):
        super(FirstWin, self).__init__()
        uic.loadUi('design/first_win.ui', self)