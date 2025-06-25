from PyQt5.QtWidgets import QDialog
from PyQt5 import uic


class PopMin(QDialog):
    def __init__(self):
        super(PopMin, self).__init__()
        uic.loadUi('pop_min.ui', self)