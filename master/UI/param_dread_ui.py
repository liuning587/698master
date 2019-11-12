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
        self.PushButton_set.clicked.connect(self.set_meter_from_tableWidget)
        self.PushButton_batchAdd.clicked.connect(self.get_metercfg_from_ui_and_set_to_table_widget)
        self.PushButton_clear.clicked.connect(self.clear_tableWidget)

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

        self.tableWidget.cellChanged.connect(self.solt_changed)
        self.tableWidget.cellClicked.connect(self.get_metercfg_from_tableWidget)
        self.tableWidget.currentCellChanged.connect(self.get_metercfg_from_tableWidget)
        self.tableWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)  ######允许右键产生子菜单
        self.tableWidget.customContextMenuRequested.connect(self.generate_tableWidgetMenu)  ####右键菜单

        self.set_metercfg_to_ui()

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

        self.tableWidget.selectRow(row_pos) #最好不要影响之前已经选择的行
        
        for col in range(self.tableWidget.columnCount()):
            self.tableWidget.item(row_pos, col).setBackground(QtCore.Qt.yellow)

    def solt_changed(self, row = -1, column = -1):
        # if row >= 0 and self.tableWidget.item(row, column) is not None:
        #     self.tableWidget.item(row, column).setBackground(QtCore.Qt.yellow)
        pass

    def get_metercfg_from_tableWidget(self, row = -1):
        mcfg = MeterCfg()

        #cfg_no
        if self.tableWidget.item(row, 0) is not None:
            mcfg.set_cfg_no(int(self.tableWidget.item(row, 0).text()))
        
        #maddr
        if self.tableWidget.item(row, 1) is not None:
            mcfg.set_maddr(self.tableWidget.item(row, 1).text())

        #baudrate
        if self.tableWidget.item(row, 2) is not None:
            if '300' in self.tableWidget.item(row, 2).text():
                mcfg.set_baudrate(0)
            elif '1200' in self.tableWidget.item(row, 2).text():
                mcfg.set_baudrate(2)
            elif '2400' in self.tableWidget.item(row, 2).text():
                mcfg.set_baudrate(3)
            elif '4800' in self.tableWidget.item(row, 2).text():
                mcfg.set_baudrate(4)
            elif '7200' in self.tableWidget.item(row, 2).text():
                mcfg.set_baudrate(5)
            elif '9600' in self.tableWidget.item(row, 2).text():
                mcfg.set_baudrate(6)
            elif '19200' in self.tableWidget.item(row, 2).text():
                mcfg.set_baudrate(7)
            elif '38400' in self.tableWidget.item(row, 2).text():
                mcfg.set_baudrate(8)
            elif '57600' in self.tableWidget.item(row, 2).text():
                mcfg.set_baudrate(9)
            elif '115200' in self.tableWidget.item(row, 2).text():
                mcfg.set_baudrate(10)
            elif '600' in self.tableWidget.item(row, 2).text():
                mcfg.set_baudrate(1)
            elif '自' in self.tableWidget.item(row, 2).text():
                mcfg.set_baudrate(255)
            else:
                mcfg.set_baudrate(3)
            
        #port
        if self.tableWidget.item(row, 3) is not None:
            if  "485-1" in self.tableWidget.item(row, 3).text():
                mcfg.set_port(0xF2010201)
            elif  "485-2" in self.tableWidget.item(row, 3).text():
                mcfg.set_port(0xF2010202)
            elif  "485-3" in self.tableWidget.item(row, 3).text():
                mcfg.set_port(0xF2010203)
            elif  "PLC" in self.tableWidget.item(row, 3).text():
                mcfg.set_port(0xF2090201)
            elif  "交采" in self.tableWidget.item(row, 3).text():
                mcfg.set_port(0xF2080201)
            else:
                mcfg.set_port(0xF2090201)

        #ptl
        if self.tableWidget.item(row, 4) is not None:
            if  "未知" in self.tableWidget.item(row, 4).text():
                mcfg.set_ptl(0)
            elif  "97" in self.tableWidget.item(row, 4).text():
                mcfg.set_ptl(1)
            elif  "07" in self.tableWidget.item(row, 4).text():
                mcfg.set_ptl(2)
            elif  "698" in self.tableWidget.item(row, 4).text():
                mcfg.set_ptl(3)
            elif  "188" in self.tableWidget.item(row, 4).text():
                mcfg.set_ptl(4)
            else:
                mcfg.set_ptl(2)

        #rate
        if self.tableWidget.item(row, 5) is not None:
            mcfg.set_rate(int(self.tableWidget.item(row, 5).text()))

        #pwd
        if self.tableWidget.item(row, 6) is not None:
            mcfg.set_pwd(self.tableWidget.item(row, 6).text())

        #lineMode
        if self.tableWidget.item(row, 7) is not None:
            if "未知" in self.tableWidget.item(row, 7).text():
                mcfg.set_lineMode(0)
            elif "单相" in self.tableWidget.item(row, 7).text():
                mcfg.set_lineMode(1)
            elif "三相三线" in self.tableWidget.item(row, 7).text():
                mcfg.set_lineMode(2)
            elif "三相四线" in self.tableWidget.item(row, 7).text():
                mcfg.set_lineMode(3)
            else:
                mcfg.set_lineMode(1)
        
        #usrType
        if self.tableWidget.item(row, 8) is not None:
            mcfg.set_usrType(int(self.tableWidget.item(row, 8).text()))

        #stdV
        if self.tableWidget.item(row, 9) is not None:
            mcfg.set_stdV(int(float(self.tableWidget.item(row, 9).text())*10 + 0.5))

        #stdA
        if self.tableWidget.item(row, 10) is not None:
            mcfg.set_stdA(int(float(self.tableWidget.item(row, 10).text())*10 + 0.5))

        #set_assetNumber
        if self.tableWidget.item(row, 11) is not None:
            mcfg.set_assetNumber(self.tableWidget.item(row, 11).text())

        #set_collAddr
        if self.tableWidget.item(row, 12) is not None:
            mcfg.set_collAddr(self.tableWidget.item(row, 12).text())

        #PT
        if self.tableWidget.item(row, 13) is not None:
            mcfg.set_PT(int(self.tableWidget.item(row, 13).text()))

        #CT
        if self.tableWidget.item(row, 14) is not None:
            mcfg.set_CT(int(self.tableWidget.item(row, 14).text()))

        self.set_metercfg_to_ui(mcfg)
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

    def clear_tableWidget(self):
        self.tableWidget.setRowCount(0)

    def generate_tableWidgetMenu(self, pos):
        menu = QtWidgets.QMenu()
        item1 = menu.addAction("下发")
        item2 = menu.addAction("删除")
        action = menu.exec_(self.tableWidget.mapToGlobal(pos))

        row_nums = []
        for row in self.tableWidget.selectionModel().selection().indexes():
            row_nums.append(row.row())
        row_nums = list(set(row_nums)) #去重

        if action == item1:
            self.set_meter_from_tableWidget()
            pass

        elif action == item2:
            row_nums.sort(reverse=True) #删除需要降序
            for r in row_nums:
                self.tableWidget.removeRow(r)
        else:
            return

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

    def set_meter_list(self, metercfg_list: [MeterCfg]):
        cnt = len(metercfg_list)
        if cnt <= 0:
            return
    
        apdu_text = '0701016000800001%02X' % cnt
        for i in range(cnt):
            apdu_text += metercfg_list[i].encode_to_str()
        apdu_text += '00'
        config.MASTER_WINDOW.se_apdu_signal.emit(apdu_text)
        pass
    
    def set_meter_thread(self, metercfg_list: [MeterCfg], max_cnt = 20, delay = 0.1):
        total = len(metercfg_list)
        no = 0

        while total > 0:
            cur = total if total < max_cnt else max_cnt
            total -= cur
            apdu_text = '0701016000800001%02X' % cur
            for i in range(cur):
                apdu_text += metercfg_list[no + i].encode_to_str()
            apdu_text += '00'
            config.MASTER_WINDOW.se_apdu_signal.emit(apdu_text)
            if total > 0:
                time.sleep(delay)
            no += cur
        pass
    
    def set_meter_from_tableWidget(self):
        ''' 搜索当前已选中的行, 生成MeterCfg列表 '''
        
        row_nums = []
        for row in self.tableWidget.selectionModel().selection().indexes():
            row_nums.append(row.row())
        row_nums = list(set(row_nums)) #去重
    
        print('待下发行:', row_nums)

        total = len(row_nums)
        if total <= 0:
            return
        max_cnt = int(self.lineEdit_cnt.text())
        if max_cnt <= 0 or max_cnt > 50:
            max_cnt = 1

        if int(self.lineEdit_delay.text()) == 0:
            delay = 0.1
        else:
            delay = float(self.lineEdit_delay.text()) / 1000 #ms

        no = 0
        while total > 0:
            cur = total if total < max_cnt else max_cnt
            total -= cur

            metercfg_list = []
            for i in range(cur):
                metercfg_list.append(self.get_metercfg_from_tableWidget(row_nums[no + i]))
                for col in range(self.tableWidget.columnCount()):
                    self.tableWidget.item(row_nums[no + i], col).setBackground(QtCore.Qt.magenta)

            self.set_meter_list(metercfg_list)
            for i in range(cur):
                for col in range(self.tableWidget.columnCount()):
                    self.tableWidget.item(row_nums[no + i], col).setBackground(QtCore.Qt.green)
            if total > 0:
                time.sleep(delay)
            no += cur
        pass

    def set_meter_list_test(self): #todo: 最好新开线程处理, 否则影响界面
        ''' just for test '''
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
