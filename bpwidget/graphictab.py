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
from signalmgr import GetSignal
from editdata import define as eddefine


class CBPTabWidget(QtWidgets.QTabWidget):
    m_Filter = "*.xh"
    m_BPDir = "./bpfile"

    def __init__(self, bpID, parent=None):
        super(CBPTabWidget, self).__init__(parent)
        self.m_BPID = bpID
        self.setMovable(True)
        self.m_GraphicUI = {}
        self.m_ShowID = 0
        self._InitSignal()

    def _InitSignal(self):
        self.currentChanged.connect(self.S_OnBPTabChange)
        GetSignal().NEW_GRAPHIC.connect(self.S_NewGraphic)

    def S_NewGraphic(self, bpID, graphicID):
        if self.m_BPID != bpID:
            return
        if graphicID in self.m_GraphicUI:
            oView = self.currentWidget()
            iIndex = self.indexOf(oView)
            self.setCurrentIndex(iIndex)
            return
        bpView = view.CBlueprintView(graphicID)
        sTabTitle = interface.GetGraphicAttr(graphicID, eddefine.GraphicAttrName.NAME)
        tabIndex = self.addTab(bpView, sTabTitle)
        self.setCurrentIndex(tabIndex)
        self.m_GraphicUI[graphicID] = bpView

        btn = QtWidgets.QPushButton("x")
        btn.setFlat(True)
        btn.setMaximumSize(16, 16)
        func = functor.Functor(self.S_CloseTab, graphicID)
        btn.clicked.connect(func)
        self.tabBar().setTabButton(tabIndex, QtWidgets.QTabBar.RightSide, btn)

    def S_CloseTab(self, graphicID, _):
        oView = self.m_GraphicUI.pop(graphicID, None)
        if not oView:
            return
        iIndex = self.indexOf(oView)
        self.removeTab(iIndex)
        self.setCurrentIndex(self.count() - 1)

    def S_OnBPTabChange(self):
        oView = self.currentWidget()
        graphicID = oView.GetGraphicID()
        GetStatusMgr().SetCurGraphicID(graphicID)
