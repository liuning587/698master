"""param dread ui"""
import os
from master import config
# from master.trans import common
from master.UI.param_dread_window import Ui_ParamDreadWindow
# from master.UI import param
# from master.datas import base_data
if config.IS_USE_PYSIDE:
    from PySide2 import QtGui, QtCore, QtWidgets
else:
    from PyQt5 import QtGui, QtCore, QtWidgets


class ParamDreadWindow(QtWidgets.QMainWindow, Ui_ParamDreadWindow):
    def __init__(self):
        super(ParamDreadWindow, self).__init__()
        self.setupUi(self)
