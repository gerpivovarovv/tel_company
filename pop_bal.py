from PyQt5.QtWidgets import QWidget
from PyQt5 import uic


class PopBal(QWidget):
    def __init__(self):
        super(PopBal, self).__init__()
        uic.loadUi('design/pop_bal.ui', self)
