# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2019-01-08 15:16:36
@Desc: 主界面
"""

import mainview

from PyQt5.QtWidgets import QTabWidget


class CMainWindow(QTabWidget):
    def __init__(self, parent=None):
        super(CMainWindow, self).__init__(parent)
        self._InitUI()
        self._InitSignal()

    def _InitUI(self):
        self.showMaximized()
        self.setWindowTitle("蓝图编辑器")
        oMainTab = mainview.CMainView(self)
        self.addTab(oMainTab, "主窗口")

    def _InitSignal(self):
        pass
