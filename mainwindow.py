# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2019-01-08 15:16:36
@Desc: 主界面
"""

import os

from PyQt5.QtWidgets import QTabWidget, QPushButton, QTabBar, QFileDialog

from signalmgr import GetSignal
from pubcode.functor import Functor
from editdata import interface
from mainwidget import mainview
from bpwidget import blueprintview


class CMainWindow(QTabWidget):
    m_Filter = "*.xh"
    m_BPDir = "./bpfile"

    def __init__(self, parent=None):
        super(CMainWindow, self).__init__(parent)
        self.m_BPInfo = {}
        self.m_BPID2Path = {}
        self.m_Path2BPID = {}
        self.m_ID = 0
        self._InitUI()
        self._InitSignal()

    def _InitUI(self):
        self.showMaximized()
        self.setMovable(True)
        self.setWindowTitle("蓝图编辑器")
        oMainTab = mainview.CMainView(self)
        self.addTab(oMainTab, "主窗口")

    def _InitSignal(self):
        GetSignal().UI_NEW_BLUEPRINT.connect(self.S_NewBlueprint)
        GetSignal().UI_SAVE_BLUEPRINT.connect(self.S_SaveBlueprint)
        GetSignal().UI_OPEN_BLUEPRINT.connect(self.S_OpenBlueprint)

    def _NewID(self):
        self.m_ID += 1
        return self.m_ID

    def S_NewBlueprint(self, bpID):
        oBPView = blueprintview.CBlueprintView(bpID, self)
        sPath = self.m_BPID2Path.get(bpID, None)
        if sPath:
            tabName = os.path.split(sPath)[1]
        else:
            tabName = "蓝图-%s" % self._NewID()
        iIndex = self.addTab(oBPView, tabName)
        self.setCurrentIndex(iIndex)
        self.setTabToolTip(iIndex, sPath)
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

    def S_OpenBlueprint(self, sPath=None):
        if not sPath:
            sPath = QFileDialog.getOpenFileName(self, "打开蓝图", self.m_BPDir, filter=self.m_Filter)[0]
            if not sPath:
                return
        if sPath in self.m_Path2BPID:
            bpID = self.m_Path2BPID[sPath]
            self._ChangeBPIndex(bpID)
            return
        bpID = interface.OpenBlueprint(sPath)
        self.m_Path2BPID[sPath] = bpID
        self.m_BPID2Path[bpID] = sPath
        self.S_NewBlueprint(bpID)

    def _ChangeBPIndex(self, bpID):
        oView = self.m_BPInfo.get(bpID, None)
        if oView:
            iIndex = self.indexOf(oView)
            self.setCurrentIndex(iIndex)

    def S_SaveBlueprint(self, bpID):
        sPath = self.m_BPID2Path.get(bpID, None)
        if not sPath:
            sPath = QFileDialog.getSaveFileName(self, "保存蓝图", self.m_BPDir, filter=self.m_Filter)[0]
            if not sPath:
                return
        interface.SaveBlueprint(bpID, sPath)
