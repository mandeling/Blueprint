# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2019-01-21 15:48:39
@Desc: 
1. 右键自定义菜单，里面添加lineedit无法输入中文问题 2019-01-21
2. 修复了之后ubuntu下运行lineedit无法输入，window正常
"""
import sys

from PyQt5.QtWidgets import QMenu, QWidget, QHBoxLayout, QLineEdit, QApplication
from PyQt5.QtCore import Qt, QSize


class CMainWindow(QWidget):
    def __init__(self, parent=None):
        super(CMainWindow, self).__init__(parent)
        self.InitUI()

    def InitUI(self):
        # self.setWindowFlags(Qt.Popup | Qt.Sheet)
        hbox = QHBoxLayout(self)
        line = QLineEdit(self)
        hbox.addWidget(line)

    # def contextMenuEvent(self, event):
    #     self.m_Menu = CMenu()
    #     pos = self.mapToGlobal(event.pos())
    #     self.m_Menu.move(pos.x(), pos.y())
    #     self.m_Menu.show()


class CMenu(QMenu):
    def __init__(self, parent=None):
        super(CMenu, self).__init__(parent)
        self.InitUI()

    def InitUI(self):
        self.setWindowFlags(Qt.Popup | Qt.Sheet)
        hbox = QHBoxLayout(self)
        line = QLineEdit(self)
        hbox.addWidget(line)

    def sizeHint(self):
        return QSize(200, 50)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    obj = CMainWindow()
    obj.show()
    sys.exit(app.exec_())
