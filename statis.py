from PyQt5.QtWidgets import QWidget
from PyQt5 import uic


class Stat(QWidget):
    def __init__(self):
        super(Stat, self).__init__()
        uic.loadUi('stat.ui', self)
