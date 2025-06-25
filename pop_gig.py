from PyQt5.QtWidgets import QDialog
from PyQt5 import uic


class PopGig(QDialog):
    def __init__(self):
        super(PopGig, self).__init__()
        uic.loadUi('pop_gig.ui', self)