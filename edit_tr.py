from PyQt5.QtWidgets import QWidget
from PyQt5 import uic


class EditTar(QWidget):
    def __init__(self):
        super(EditTar, self).__init__()
        uic.loadUi('design/edit_tr.ui', self)
