# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-12-10 10:08:56
@Desc: 蓝图tabwidget
"""

import os

from PyQt5 import QtWidgets

from graphics import view
from graphics.uimgr import GetUIMgr
from editdata import interface
from pubcode import functor


class CBPTabWidget(QtWidgets.QTabWidget):
    m_Filter = "*.xh"

    def __init__(self, parent=None):
        super(CBPTabWidget, self).__init__(parent)
        self.setMovable(True)
        self.m_ShowID = 0
        self.m_PathInfo = {}

    def NewBlueprint(self, sPath=None):
        if sPath:
            bpID = interface.OpenBlueprint(sPath)
            bpView = view.CBlueprintView(bpID)
            sTabTitle = os.path.split(sPath)[1]
            tabIndex = self.addTab(bpView, sTabTitle)
            self.setTabToolTip(tabIndex, sPath)
        else:
            bpID = interface.NewBlueprint()
            bpView = view.CBlueprintView(bpID)
            self.m_ShowID += 1
            sTabTitle = "蓝图%s" % self.m_ShowID
            tabIndex = self.addTab(bpView, sTabTitle)

        self.setCurrentIndex(tabIndex)
        self.m_PathInfo[bpID] = sPath

        btn = QtWidgets.QPushButton("x")
        btn.setFlat(True)
        btn.setMaximumSize(16, 16)
        func = functor.Functor(self.S_CloseTab, bpID)
        btn.clicked.connect(func)
        self.tabBar().setTabButton(tabIndex, QtWidgets.QTabBar.RightSide, btn)

    def OpenBlueprint(self):
        sPath = QtWidgets.QFileDialog.getOpenFileName(self, "打开蓝图", filter=self.m_Filter)[0]
        if sPath:
            self.NewBlueprint(sPath)

    def SaveBlueprint(self):
        oView = self.currentWidget()
        bpID = oView.GetBPID()
        sPath = self.m_PathInfo.get(bpID, None)
        if not sPath:
            sPath = QtWidgets.QFileDialog.getSaveFileName(self, "保存蓝图", filter=self.m_Filter)[0]
            if not sPath:
                return
        interface.SaveBlueprint(bpID, sPath)
        sTabTitle = os.path.split(sPath)[1]
        iIndex = self.indexOf(oView)
        self.setTabText(iIndex, sTabTitle)
        self.setTabToolTip(iIndex, sPath)

    def S_CloseTab(self, bpID, _):
        oView = GetUIMgr().GetBPView(bpID)
        if not oView:
            return
        iIndex = self.indexOf(oView)
        self.removeTab(iIndex)
        self.setCurrentIndex(self.count() - 1)
        if bpID in self.m_PathInfo:
            del self.m_PathInfo[bpID]
        GetUIMgr().DelBPView(bpID)
