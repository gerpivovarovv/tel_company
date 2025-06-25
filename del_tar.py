from PyQt5.QtWidgets import QWidget
from PyQt5 import uic


class DelTar(QWidget):
    def __init__(self):
        super(DelTar, self).__init__()
        uic.loadUi('design/del_tar.ui', self)
