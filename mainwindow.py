# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2019-01-08 15:16:36
@Desc: 主界面
"""

import blueprintview
import mainview

from PyQt5.QtWidgets import QTabWidget, QPushButton, QTabBar
from signalmgr import GetSignal
from pubcode.functor import Functor


class CMainWindow(QTabWidget):
    def __init__(self, parent=None):
        super(CMainWindow, self).__init__(parent)
        self.m_BPInfo = {}
        self.m_ID = 0
        self._InitUI()
        self._InitSignal()

    def _InitUI(self):
        self.showMaximized()
        self.setWindowTitle("蓝图编辑器")
        oMainTab = mainview.CMainView(self)
        self.addTab(oMainTab, "主窗口")

    def _InitSignal(self):
        GetSignal().NEW_BLUEPRINT.connect(self.S_NewBlueprint)

    def _NewID(self):
        self.m_ID += 1
        return self.m_ID

    def S_NewBlueprint(self, bpID):
        oBPView = blueprintview.CBlueprintView(bpID, self)
        sName = "蓝图-%s" % self._NewID()
        iIndex = self.addTab(oBPView, sName)
        self.setCurrentIndex(iIndex)
        self.m_BPInfo[bpID] = oBPView

        btn = QPushButton("x")
        btn.setFlat(True)
        btn.setMaximumSize(16, 16)
        func = Functor(self.S_CloseTab, bpID)
        btn.clicked.connect(func)
        self.tabBar().setTabButton(iIndex, QTabBar.RightSide, btn)

    def S_CloseTab(self, bpID, _):
        oBPView = self.m_BPInfo.pop(bpID, None)
        if not oBPView:
            return
        iIndex = self.indexOf(oBPView)
        self.removeTab(iIndex)
        self.setCurrentIndex(self.count() - 1)
