from PyQt5.QtWidgets import QWidget
from PyQt5 import uic


class EditNumb(QWidget):
    def __init__(self):
        super(EditNumb, self).__init__()
        uic.loadUi('edit_numb.ui', self)
