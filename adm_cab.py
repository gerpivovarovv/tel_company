from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic


class AdmCab(QMainWindow):
    def __init__(self):
        super(AdmCab, self).__init__()
        uic.loadUi('adm_cab.ui', self)