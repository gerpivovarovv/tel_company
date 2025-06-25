from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic


class WinAv(QMainWindow):
    def __init__(self):
        super(WinAv, self).__init__()
        uic.loadUi('avtor.ui', self)