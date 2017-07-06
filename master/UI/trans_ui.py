"""log files trans ui"""
import re
import os
import sys
import threading
import chardet
from PyQt4 import QtCore, QtGui
from master.UI.ui_setup import TransWindowUi
from master.trans.translate import Translate
from master import config
import master.trans.common as commonfun


class TransWindow(QtGui.QMainWindow, TransWindowUi):
    """translate window"""
    load_file = QtCore.pyqtSignal(str)
    set_progress = QtCore.pyqtSignal(int)

    def __init__(self):
        super(TransWindow, self).__init__()
        self.setup_ui()
        self.setAcceptDrops(True)
        self.is_show_level = self.show_level_cb.isChecked()
        self.input_box.cursorPositionChanged.connect(self.cursor_changed)
        self.input_box.textChanged.connect(self.take_input_text)
        self.find_last_b.clicked.connect(lambda: self.find_last(True))
        self.find_next_b.clicked.connect(lambda: self.find_next(True))
        self.input_zoom_in_b.clicked.connect(self.input_box.zoomIn)
        self.input_zoom_out_b.clicked.connect(self.input_box.zoomOut)
        self.output_zoom_in_b.clicked.connect(self.output_box.zoomIn)
        self.output_zoom_out_b.clicked.connect(self.output_box.zoomOut)
        self.show_level_cb.clicked.connect(self.set_level_visible)
        self.always_top_cb.clicked.connect(self.set_always_top)
        self.open_action.triggered.connect(self.openfile)
        self.close_action.triggered.connect(self.clear_box)
        self.about_action.triggered.connect(config.ABOUT_WINDOW.show)
        self.find_action.triggered.connect(lambda: self.find_box.setFocus() or self.find_box.selectAll())
        self.load_file.connect(self.load_text, QtCore.Qt.QueuedConnection)
        self.set_progress.connect(self.set_progressbar, QtCore.Qt.QueuedConnection)
        self.connect(self.find_box, QtCore.SIGNAL("returnPressed()"), lambda: self.find_next(False))

        self.proc_bar.setVisible(False)
        self.show_level_cb.setChecked(True)

        self.msg_find_dict = []
        self.last_selection = (0, 0)
        self.text_find_list = []
        self.last_find_text = ''

    def dragEnterEvent(self, event):
        """drag"""
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        """drag"""
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        """drop file"""
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
            links = []
            for url in event.mimeData().urls():
                links.append(str(url.toLocalFile()))
            if links[0].split('.')[-1] in ['txt', 'TXT', 'log', 'LOG']:
                self.openfile(links[0])
        else:
            event.ignore()

    def load_text(self, file_text):
        """load text"""
        self.proc_bar.setVisible(False)
        self.open_action.setEnabled(True)
        self.setAcceptDrops(True)
        self.input_box.setPlainText(file_text)

    def set_progressbar(self, percent):
        """set progress bar in main process"""
        self.proc_bar.setValue(percent)

    def openfile(self, filepath=''):
        """open file"""
        if not filepath:
            filepath = QtGui.QFileDialog.getOpenFileName(self, caption='请选择698日志文件', filter='*.txt *.log')
        if filepath:
            print('filepath: ', filepath)
            file_size = os.path.getsize(filepath)
            if file_size > 3000000:
                reply = QtGui.QMessageBox.question(self, '警告', '打开大型文件会使用较长时间，确定打开吗？',\
                                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
                if reply != QtGui.QMessageBox.Yes:
                    return
            self.proc_bar.setVisible(True)
            self.open_action.setEnabled(False)
            self.setAcceptDrops(False)
            self.proc_l.setText('处理中')
            self.setWindowTitle('698日志解析工具_{ver} - {file}'.\
                        format(ver=config.MASTER_WINDOW_TITLE_ADD, file=filepath))
            threading.Thread(target=self.read_file,\
                                args=(filepath,)).start()

    def read_file(self, filepath):
        """read file thread"""
        # get file encoding
        with open(filepath, "rb") as file:
            encoding = chardet.detect(file.read(65535))
            print(encoding)
            if encoding['confidence'] > 0.95:
                file_encoding = encoding['encoding']
            else:
                file_encoding = 'gb2312'

        with open(filepath, encoding=file_encoding, errors='ignore') as file:
            count = 0
            for _ in file:
                count += 1
        print(count)
        with open(filepath, encoding=file_encoding, errors='ignore') as file:
            file_text = ''
            for i, line in enumerate(file):
                file_text += line
                if i % 500 == 0:
                    self.set_progress.emit(i*95 / count)
        self.load_file.emit(file_text)
        print('read_file thread quit')

    def cursor_changed(self):
        """cursor changed to trans"""
        print(int(self.input_box.textCursor().position()))
        if self.last_selection[0] <= int(self.input_box.textCursor().position())\
                                    <= self.last_selection[1]:
            return
        else:
            self.trans_pos(int(self.input_box.textCursor().position()))

    def trans_pos(self, message_pos):
        """trans message in position"""
        for row in self.msg_find_dict:
            # print(row)
            if row['span'][0] <= message_pos <= row['span'][1]:
                self.start_trans(row['message'])
                cursor = self.input_box.textCursor()
                cursor.setPosition(row['span'][0])
                cursor.setPosition(row['span'][1], QtGui.QTextCursor.KeepAnchor)
                self.input_box.setTextCursor(cursor)
                self.last_selection = row['span']
                break
        else:
            self.output_box.setText('请点选一条报文')
            self.last_selection = (0, 0)

    def take_input_text(self):
        """handle with input text"""
        input_text = self.input_box.toPlainText()
        res = re.compile(r'([0-9a-fA-F]{2} ){5,}[0-9a-fA-F]{2}')
        all_match = res.finditer(input_text)
        self.msg_find_dict = []
        find_num = 0
        for mes in all_match:
            self.msg_find_dict += [{'message': mes.group(), 'span': mes.span()}]
            find_num += 1
        self.proc_l.setText('找到报文%d条'%find_num)
        if len(self.msg_find_dict) == 1 and self.msg_find_dict[0]['message'].strip() == input_text.strip():
            self.start_trans(self.msg_find_dict[0]['message'])

        self.find_l.setText('')

    def start_trans(self, input_text):
        """start_trans"""
        trans = Translate(input_text)
        brief = trans.get_brief()
        full = trans.get_full(self.is_show_level)
        self.output_box.setText(r'<b>【概览】</b><p>%s</p><hr><b>【完整】</b>%s'%(brief, full))

    def clear_box(self):
        """clear_box"""
        self.input_box.setText('')
        self.output_box.setText('')
        self.setWindowTitle('698日志解析工具_{ver}'.format(ver=config.MASTER_WINDOW_TITLE_ADD))
        self.input_box.setFocus()

    def search_text(self, text):
        """search_text"""
        input_text = self.input_box.toPlainText()
        res = re.compile(r'%s'%text)
        all_match = res.finditer(input_text)
        self.text_find_list = [mes.span() for mes in all_match]
        if self.text_find_list:
            self.find_l.setText('0/%d'%len(self.text_find_list))
        else:
            self.find_l.setText('未找到！')

    def find_next(self, is_setfocus=True):
        """find_next"""
        find_text = self.find_box.text()
        if not find_text:
            return
        if self.find_l.text() == '' or find_text != self.last_find_text:
            self.search_text(find_text)
        if self.find_l.text() == '未找到！':
            return
        cursor = self.input_box.textCursor()
        position = cursor.position()
        for count, text_find in enumerate(self.text_find_list, 1):
            if text_find[0] >= position:
                self.find_l.setText('%d/'%count + self.find_l.text().split('/')[1])
                cursor.setPosition(text_find[0])
                cursor.setPosition(text_find[1], QtGui.QTextCursor.KeepAnchor)
                self.input_box.setTextCursor(cursor)
                break
        else:
            self.find_l.setText('1/' + self.find_l.text().split('/')[1])
            cursor.setPosition(self.text_find_list[0][0])
            cursor.setPosition(self.text_find_list[0][1], QtGui.QTextCursor.KeepAnchor)
            self.input_box.setTextCursor(cursor)
        if is_setfocus:
            self.input_box.setFocus()

    def find_last(self, is_setfocus=True):
        """find_last"""
        find_text = self.find_box.text()
        if not find_text:
            return
        if self.find_l.text() or find_text != self.last_find_text:
            self.search_text(find_text)
        if self.find_l.text() == '未找到！':
            return
        cursor = self.input_box.textCursor()
        position = cursor.position()
        for count, text_find in enumerate(self.text_find_list[::-1], 0):
            if text_find[1] < position:
                self.find_l.setText('%d/'%(len(self.text_find_list) - count)\
                                        + self.find_l.text().split('/')[1])
                cursor.setPosition(text_find[0])
                cursor.setPosition(text_find[1], QtGui.QTextCursor.KeepAnchor)
                self.input_box.setTextCursor(cursor)
                break
        else:
            self.find_l.setText('%d/%d'%(len(self.text_find_list),\
                                    len(self.text_find_list)))
            cursor.setPosition(self.text_find_list[::-1][0][0])
            cursor.setPosition(self.text_find_list[::-1][0][1], QtGui.QTextCursor.KeepAnchor)
            self.input_box.setTextCursor(cursor)
        if is_setfocus:
            self.input_box.setFocus()

    def set_level_visible(self):
        """set_level_visible"""
        self.is_show_level = self.show_level_cb.isChecked()
        self.trans_pos(int(self.input_box.textCursor().position()))

    def set_always_top(self):
        """set_always_top"""
        window_pos = self.pos()
        if self.always_top_cb.isChecked() is True:
            self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
            self.show()
        else:
            self.setWindowFlags(QtCore.Qt.Widget)
            self.show()
        self.move(window_pos)


if __name__ == '__main__':
    APP = QtGui.QApplication(sys.argv)
    dialog = TransWindow()
    dialog.show()
    APP.exec_()
    os._exit(0)