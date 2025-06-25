from PyQt5.QtWidgets import QWidget
from PyQt5 import uic


class CrTar(QWidget):
    def __init__(self):
        super(CrTar, self).__init__()
        uic.loadUi('design/cr_tar.ui', self)
