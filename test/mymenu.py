# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2019-01-21 15:48:39
@Desc: 右键自定义菜单，里面添加lineedit无法输入中文问题
"""
import sys

from PyQt5.QtWidgets import QMenu, QWidget, QHBoxLayout, QLineEdit, QApplication


class CMainWindow(QWidget):
    def __init__(self, parent=None):
        super(CMainWindow, self).__init__(parent)

    def contextMenuEvent(self, event):
        menu = CMenu()
        pos = self.mapToGlobal(event.pos())
        menu.move(pos.x(), pos.y())
        menu.exec_()


class CMenu(QMenu):
    def __init__(self, parent=None):
        super(CMenu, self).__init__(parent)
        self.InitUI()

    def InitUI(self):
        hbox = QHBoxLayout(self)
        line = QLineEdit(self)
        hbox.addWidget(line)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    obj = CMainWindow()
    obj.show()
    sys.exit(app.exec_())
