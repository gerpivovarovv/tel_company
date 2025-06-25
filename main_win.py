from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic


class PersCab(QMainWindow):
    def __init__(self):
        super(PersCab, self).__init__()
        uic.loadUi('main_win.ui', self)