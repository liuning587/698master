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
        self.PushButton_batchAdd.clicked.connect(self.get_metercfg_from_ui_and_set_to_table_widget)
        #tableWidget
        items = ['序号', '通信地址', '波特率', '端口', '规约类型', '费率', '通信密码', '接线方式', '用户类型', '额定电压', '额定电流', '资产号', '采集器地址', 'PT', 'CT']
        for count in range(len(items)):
            self.tableWidget.insertColumn(count)
        self.tableWidget.setHorizontalHeaderLabels(items)
        self.tableWidget.setColumnWidth(0, 40)   #序号
        self.tableWidget.setColumnWidth(1, 110)  #通信地址
        self.tableWidget.setColumnWidth(2, 55)   #波特率
        self.tableWidget.setColumnWidth(3, 50)   #端口
        self.tableWidget.setColumnWidth(4, 80)   #规约类型
        self.tableWidget.setColumnWidth(5, 40)   #费率
        self.tableWidget.setColumnWidth(6, 110)  #通信密码
        self.tableWidget.setColumnWidth(7, 70)   #接线方式
        self.tableWidget.setColumnWidth(8, 65)   #用户类型
        self.tableWidget.setColumnWidth(9, 65)   #额定电压
        self.tableWidget.setColumnWidth(10, 65)  #额定电流
        self.tableWidget.setColumnWidth(11, 110) #资产号
        self.tableWidget.setColumnWidth(12, 110) #采集器地址
        self.tableWidget.setColumnWidth(13, 40)  #PT
        self.tableWidget.setColumnWidth(14, 40)  #CT

        # self.add_meter_to_tableWidget()
        # mcfg = MeterCfg()
        # mcfg.set_maddr("%012d"%5)
        # self.set_metercfg_to_ui(mcfg)

    def add_meter_to_tableWidget(self, mcfg = MeterCfg(), row_pos = -1):
        if row_pos == -1:
            row_pos = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_pos)

        self.tableWidget.setItem(row_pos, 0,  QtWidgets.QTableWidgetItem(mcfg.get_cfg_no()))
        self.tableWidget.setItem(row_pos, 1,  QtWidgets.QTableWidgetItem(mcfg.get_maddr()))
        self.tableWidget.setItem(row_pos, 2,  QtWidgets.QTableWidgetItem(mcfg.get_baudrate()))
        self.tableWidget.setItem(row_pos, 3,  QtWidgets.QTableWidgetItem(mcfg.get_port()))
        self.tableWidget.setItem(row_pos, 4,  QtWidgets.QTableWidgetItem(mcfg.get_ptl()))
        self.tableWidget.setItem(row_pos, 5,  QtWidgets.QTableWidgetItem(mcfg.get_rate()))
        self.tableWidget.setItem(row_pos, 6,  QtWidgets.QTableWidgetItem(mcfg.get_pwd()))
        self.tableWidget.setItem(row_pos, 7,  QtWidgets.QTableWidgetItem(mcfg.get_lineMode()))
        self.tableWidget.setItem(row_pos, 8,  QtWidgets.QTableWidgetItem(mcfg.get_usrType()))
        self.tableWidget.setItem(row_pos, 9,  QtWidgets.QTableWidgetItem(mcfg.get_stdV()))
        self.tableWidget.setItem(row_pos, 10,  QtWidgets.QTableWidgetItem(mcfg.get_stdA()))
        self.tableWidget.setItem(row_pos, 11,  QtWidgets.QTableWidgetItem(mcfg.get_assetNumber()))
        self.tableWidget.setItem(row_pos, 12,  QtWidgets.QTableWidgetItem(mcfg.get_collAddr()))
        self.tableWidget.setItem(row_pos, 13,  QtWidgets.QTableWidgetItem(mcfg.get_PT()))
        self.tableWidget.setItem(row_pos, 14,  QtWidgets.QTableWidgetItem(mcfg.get_CT()))

        pass

    def get_meter_from_tableWidget(self, index = -1):
        mcfg = MeterCfg()
        return mcfg

    def set_metercfg_to_ui(self, mcfg = MeterCfg()):
        self.lineEdit_cfg_no.setText(mcfg.get_cfg_no())
        self.lineEdit_maddr.setText(mcfg.get_maddr())
        self.comboBox_baudrate.setCurrentIndex(mcfg.baudrate if mcfg.baudrate < 11 else 11)
        
        if mcfg.port == 0xF2010201:
            self.comboBox_port.setCurrentIndex(0)
        elif mcfg.port == 0xF2010202:
            self.comboBox_port.setCurrentIndex(1)
        elif mcfg.port == 0xF2010203:
            self.comboBox_port.setCurrentIndex(2)
        elif mcfg.port == 0xF2090201:
            self.comboBox_port.setCurrentIndex(3)
        elif mcfg.port == 0xF2080201:
            self.comboBox_port.setCurrentIndex(4)
        elif mcfg.port == 0xF2080201:
            self.comboBox_port.setCurrentIndex(-1)

        self.comboBox_ptl.setCurrentIndex(mcfg.ptl if mcfg.ptl <= 4 else 0)
        self.comboBox_rate.setCurrentText(mcfg.get_rate())
        self.lineEdit_pwd.setText(mcfg.get_pwd())
        self.comboBox_lineMode.setCurrentIndex(mcfg.lineMode if mcfg.lineMode <= 3 else 0)
        self.comboBox_usrType.setCurrentText(mcfg.get_usrType())
        self.comboBox_stdA.setCurrentText(mcfg.get_stdA())
        self.comboBox_stdV.setCurrentText(mcfg.get_stdV())
        self.lineEdit_assetNumber.setText(mcfg.get_assetNumber())
        self.lineEdit_collAddr.setText(mcfg.get_collAddr())
        self.lineEdit_PT.setText(mcfg.get_PT())
        self.lineEdit_CT.setText(mcfg.get_CT())

    def get_metercfg_from_ui(self):
        mcfg = MeterCfg()
        mcfg.set_cfg_no(int(self.lineEdit_cfg_no.text()))
        mcfg.set_maddr("%012d" % int(self.lineEdit_maddr.text()))
        baudrate = self.comboBox_baudrate.currentIndex()
        mcfg.set_baudrate(baudrate if baudrate < 11 else 11)
        
        if  "485-1" in self.comboBox_port.currentText():
            mcfg.set_port(0xF2010201)
        elif  "485-2" in self.comboBox_port.currentText():
            mcfg.set_port(0xF2010202)
        elif  "485-3" in self.comboBox_port.currentText():
            mcfg.set_port(0xF2010203)
        elif  "PLC" in self.comboBox_port.currentText():
            mcfg.set_port(0xF2090201)
        elif  "交采" in self.comboBox_port.currentText():
            mcfg.set_port(0xF2080201)
        else:
            mcfg.set_port(0xF2090201)

        ptl = self.comboBox_ptl.currentIndex()
        mcfg.set_ptl(ptl if ptl < 5 else 0)

        mcfg.set_rate(int(self.comboBox_rate.currentText()))
        mcfg.set_pwd(self.lineEdit_pwd.text())

        if "未知" in self.comboBox_lineMode.currentText():
            mcfg.set_lineMode(0)
        elif "单相" in self.comboBox_lineMode.currentText():
            mcfg.set_lineMode(1)
        elif "三相三线" in self.comboBox_lineMode.currentText():
            mcfg.set_lineMode(2)
        elif "三相四线" in self.comboBox_lineMode.currentText():
            mcfg.set_lineMode(3)
        else:
            mcfg.set_lineMode(1)

        mcfg.set_usrType(int(self.comboBox_usrType.currentText()))
        mcfg.set_stdA(int(float(self.comboBox_stdA.currentText())*10 + 0.5))
        mcfg.set_stdV(int(float(self.comboBox_stdV.currentText())*10 + 0.5))

        mcfg.set_assetNumber(self.lineEdit_assetNumber.text())
        mcfg.set_collAddr(self.lineEdit_collAddr.text())
        mcfg.set_PT(int(self.lineEdit_PT.text()))
        mcfg.set_CT(int(self.lineEdit_CT.text()))

        return mcfg

    def get_metercfg_from_ui_and_set_to_table_widget(self):
        mcfg = self.get_metercfg_from_ui()
        cnt = int(self.lineEdit_batchAdd.text())

        for _ in range(cnt):
            self.add_meter_to_tableWidget(mcfg)
            mcfg.cfg_no += 1
            mcfg.set_maddr("%012d" % (int(mcfg.get_maddr()) + 1))
        
        self.set_metercfg_to_ui(mcfg)
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