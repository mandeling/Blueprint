# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-12-10 10:08:56
@Desc: 蓝图tabwidget
"""

import os

from PyQt5 import QtWidgets

from pubcode import functor
from graphics import view
from editdata import interface
from viewmgr.uimgr import GetUIMgr
from viewmgr.statusmgr import GetStatusMgr


class CBPTabWidget(QtWidgets.QTabWidget):
    m_Filter = "*.xh"
    m_BPDir = "./bpfile"

    def __init__(self, bpID, parent=None):
        super(CBPTabWidget, self).__init__(parent)
        self.m_BPID = bpID
        self.setMovable(True)
        self.m_ShowID = 0
        self.m_BPID2Path = {}
        self.m_Path2BPID = {}
        self._InitSignal()

    def _InitSignal(self):
        self.currentChanged.connect(self.S_OnBPTabChange)

    def NewGraphic(self, sPath=None):
        if sPath:
            bpID = interface.OpenGraphic(sPath)
            bpView = view.CBlueprintView(bpID)
            sTabTitle = os.path.split(sPath)[1]
            tabIndex = self.addTab(bpView, sTabTitle)
            self.setTabToolTip(tabIndex, sPath)
        else:
            bpID = interface.NewGraphic()
            bpView = view.CBlueprintView(bpID)
            self.m_ShowID += 1
            sTabTitle = "蓝图%s" % self.m_ShowID
            tabIndex = self.addTab(bpView, sTabTitle)

        self.setCurrentIndex(tabIndex)
        self.m_BPID2Path[bpID] = sPath
        if sPath:
            self.m_Path2BPID[sPath] = bpID

        btn = QtWidgets.QPushButton("x")
        btn.setFlat(True)
        btn.setMaximumSize(16, 16)
        func = functor.Functor(self.S_CloseTab, bpID)
        btn.clicked.connect(func)
        self.tabBar().setTabButton(tabIndex, QtWidgets.QTabBar.RightSide, btn)

    def OpenGraphic(self):
        sPath = QtWidgets.QFileDialog.getOpenFileName(self, "打开蓝图", self.m_BPDir, filter=self.m_Filter)[0]
        if not sPath:
            return
        if sPath in self.m_Path2BPID:
            bpID = self.m_Path2BPID[sPath]
            self.ChangeCurIndex(bpID)
            return
        self.NewGraphic(sPath)

    def ChangeCurIndex(self, bpID):
        oView = GetUIMgr().GetGraphicView(bpID)
        iIndex = self.indexOf(oView)
        self.setCurrentIndex(iIndex)

    def SaveGraphic(self):
        oView = self.currentWidget()
        bpID = oView.GetGraphicID()
        sPath = self.m_BPID2Path.get(bpID, None)
        if not sPath:
            sPath = QtWidgets.QFileDialog.getSaveFileName(self, "保存蓝图", self.m_BPDir, filter=self.m_Filter)[0]
            if not sPath:
                return
        interface.SaveGraphic(bpID, sPath)
        sTabTitle = os.path.split(sPath)[1]
        iIndex = self.indexOf(oView)
        self.setTabText(iIndex, sTabTitle)
        self.setTabToolTip(iIndex, sPath)

    def Delete(self, bpID):
        if bpID not in self.m_BPID2Path:
            return
        sPath = self.m_BPID2Path.pop(bpID)
        if sPath in self.m_Path2BPID:
            del self.m_Path2BPID[sPath]

    def S_CloseTab(self, bpID, _):
        oView = GetUIMgr().GetGraphicView(bpID)
        if not oView:
            return
        iIndex = self.indexOf(oView)
        self.removeTab(iIndex)
        self.setCurrentIndex(self.count() - 1)
        self.Delete(bpID)
        GetUIMgr().DelGraphicView(bpID)

    def S_OnBPTabChange(self):
        oView = self.currentWidget()
        bpID = oView.GetGraphicID()
        GetStatusMgr().SetCurGraphicID(bpID)
