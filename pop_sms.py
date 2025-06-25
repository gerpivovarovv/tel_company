from PyQt5.QtWidgets import QDialog
from PyQt5 import uic


class PopSms(QDialog):
    def __init__(self):
        super(PopSms, self).__init__()
        uic.loadUi('pop_sms.ui', self)