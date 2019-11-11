"""param dread ui"""
import os
import time
from master.UI.metercfg import MeterCfg
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
        self.PushButton_set.clicked.connect(self.set_meter_list)
        #tableWidget
        items = ['', '序号', '通信地址', '波特率', '端口', '规约类型', '费率', '通信密码', '接线方式', '用户类型', '额定电压', '额定电流', '资产号', '采集器地址', 'PT', 'CT']
        for count in range(len(items)):
            self.tableWidget.insertColumn(count)
        self.tableWidget.setHorizontalHeaderLabels(items)
        self.tableWidget.setColumnWidth(0, 10)   #check
        self.tableWidget.setColumnWidth(1, 40)   #序号
        self.tableWidget.setColumnWidth(2, 110)  #通信地址
        self.tableWidget.setColumnWidth(3, 55)   #波特率
        self.tableWidget.setColumnWidth(4, 50)   #端口
        self.tableWidget.setColumnWidth(5, 80)   #规约类型
        self.tableWidget.setColumnWidth(6, 40)   #费率
        self.tableWidget.setColumnWidth(7, 110)  #通信密码
        self.tableWidget.setColumnWidth(8, 70)   #接线方式
        self.tableWidget.setColumnWidth(9, 65)   #用户类型
        self.tableWidget.setColumnWidth(10, 65)  #额定电压
        self.tableWidget.setColumnWidth(11, 65)  #额定电流
        self.tableWidget.setColumnWidth(12, 110) #资产号
        self.tableWidget.setColumnWidth(13, 110) #采集器地址
        self.tableWidget.setColumnWidth(14, 40)  #PT
        self.tableWidget.setColumnWidth(15, 40)  #CT

        self.add_meter_to_tableWidget()

    def add_meter_to_tableWidget(self, mcfg = MeterCfg()):
        row_pos = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row_pos)

        meter_enable_cb = QtWidgets.QCheckBox()
        meter_enable_cb.setChecked(True)
        self.tableWidget.setCellWidget(row_pos, 0, meter_enable_cb)

        self.tableWidget.setItem(row_pos, 1,  QtWidgets.QTableWidgetItem(mcfg.get_cfg_no()))
        self.tableWidget.setItem(row_pos, 2,  QtWidgets.QTableWidgetItem(mcfg.get_maddr()))
        self.tableWidget.setItem(row_pos, 3,  QtWidgets.QTableWidgetItem(mcfg.get_baudrate()))
        self.tableWidget.setItem(row_pos, 4,  QtWidgets.QTableWidgetItem(mcfg.get_port()))
        self.tableWidget.setItem(row_pos, 5,  QtWidgets.QTableWidgetItem(mcfg.get_ptl()))
        self.tableWidget.setItem(row_pos, 6,  QtWidgets.QTableWidgetItem(mcfg.get_rate()))
        self.tableWidget.setItem(row_pos, 7,  QtWidgets.QTableWidgetItem(mcfg.get_pwd()))
        self.tableWidget.setItem(row_pos, 8,  QtWidgets.QTableWidgetItem(mcfg.get_lineMode()))
        self.tableWidget.setItem(row_pos, 9,  QtWidgets.QTableWidgetItem(mcfg.get_usrType()))
        self.tableWidget.setItem(row_pos, 10,  QtWidgets.QTableWidgetItem(mcfg.get_stdV()))
        self.tableWidget.setItem(row_pos, 11,  QtWidgets.QTableWidgetItem(mcfg.get_stdA()))
        self.tableWidget.setItem(row_pos, 12,  QtWidgets.QTableWidgetItem(mcfg.get_assetNumber()))
        self.tableWidget.setItem(row_pos, 13,  QtWidgets.QTableWidgetItem(mcfg.get_collAddr()))
        self.tableWidget.setItem(row_pos, 14,  QtWidgets.QTableWidgetItem(mcfg.get_PT()))
        self.tableWidget.setItem(row_pos, 15,  QtWidgets.QTableWidgetItem(mcfg.get_CT()))

        pass

    def get_meter_list(self):
        apdu_text = '0501016000020000'
        config.MASTER_WINDOW.se_apdu_signal.emit(apdu_text)
        config.MASTER_WINDOW.receive_signal.connect(self.re_get_meter_list)
    
    def re_get_meter_list(self, re_text):
        config.MASTER_WINDOW.receive_signal.disconnect(self.re_get_meter_list)
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

    def set_meter_list(self):
        total = 2000
        MAX_CNT = 20
        meter = MeterCfg()
        no = 0

        while total > 0:
            cur = total if total < MAX_CNT else MAX_CNT
            total -= cur
            apdu_text = '0701016000800001%02X' % cur
            for _ in range(0, cur):
                meter.set_cfg_no(no + 2)
                meter.set_maddr('%012d' % (no + 1))
                no += 1
                apdu_text += meter.encode_to_str()
            apdu_text += '00'
            config.MASTER_WINDOW.se_apdu_signal.emit(apdu_text)
            # time.sleep(0.1)