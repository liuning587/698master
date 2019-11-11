"""param dread ui"""
import os
from master import config
from master.trans import common
from master.UI.param_dread_window import Ui_ParamDreadWindow
from master.UI import param
from master.datas import base_data
if config.IS_USE_PYSIDE:
    from PySide2 import QtGui, QtCore, QtWidgets
else:
    from PyQt5 import QtGui, QtCore, QtWidgets


class ParamDreadWindow(QtWidgets.QMainWindow, Ui_ParamDreadWindow):
    def __init__(self):
        super(ParamDreadWindow, self).__init__()
        self.setupUi(self)

        self.setWindowTitle('抄表配置')
        self.setWindowIcon(QtGui.QIcon(os.path.join(config.SOFTWARE_PATH, config.MASTER_ICO_PATH)))
        self.PushButton_get.clicked.connect(self.get_meter_list)

    def get_meter_list(self):
        apdu_text = '0501016000020000'
        config.MASTER_WINDOW.se_apdu_signal.emit(apdu_text)
        config.MASTER_WINDOW.receive_signal.connect(self.re_get_meter_list)
    
    def re_get_meter_list(self, re_text):
        m_data = common.text2list(re_text)
        data = common.get_apdu_list(m_data)
        print('recv: ', data)
        # offset = 7
        # if data[offset] == '01':
        #     self.res_b.setStyleSheet('color: green')
        #     self.res_b.setText('成功')
        #     offset += 2
        #     DT_read = QtCore.QDateTime(
        #         (int(data[offset], 16) << 8) | int(data[offset + 1], 16),
        #         int(data[offset + 2], 16),
        #         int(data[offset + 3], 16),
        #         int(data[offset + 4], 16),
        #         int(data[offset + 5], 16),
        #         int(data[offset + 6], 16),
        #     )
        #     # print('DT_read', DT_read)
        #     self.DT_box.setDateTime(DT_read)
        # else:
        #     self.res_b.setStyleSheet('color: red')
        #     self.res_b.setText('失败：' + base_data.get_dar(int(data[offset + 1], 16)))
        config.MASTER_WINDOW.receive_signal.disconnect(self.re_get_meter_list)