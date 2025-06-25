from PyQt5.QtWidgets import QDialog
from PyQt5 import uic


class ChTar(QDialog):
    def __init__(self):
        super(ChTar, self).__init__()
        uic.loadUi('design/tariph.ui', self)