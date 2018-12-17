# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-12-10 10:08:56
@Desc: 蓝图tabwidget
"""

import os
from PyQt5 import QtWidgets
from . import view
from editdata import interface

# class CBlueprintWidget(QtWidgets.QWidget):
#     def __init__(self, parent=None):
#         super(CBlueprintWidget, self).__init__(parent)
#         self.BPtabWidget = None
#         self.InitUI()

#     def InitUI(self):
#         verticalLayout = QtWidgets.QVBoxLayout(self)
#         horizontalLayout = QtWidgets.QHBoxLayout()
#         self.m_BtnCompile = QtWidgets.QPushButton("编译", self)
#         horizontalLayout.addWidget(self.m_BtnCompile)
#         self.m_BtnStart = QtWidgets.QPushButton("开始", self)
#         horizontalLayout.addWidget(self.m_BtnStart)
#         self.m_BtnDebug = QtWidgets.QPushButton("调试", self)
#         horizontalLayout.addWidget(self.m_BtnDebug)
#         verticalLayout.addLayout(horizontalLayout)
#         self.BPtabWidget = CBlueprintView(self)
#         verticalLayout.addWidget(self.BPtabWidget)

#     def NewBlueprint(self):
#         self.BPtabWidget.AddBlueprint()

#     def SaveBlueprint(self):
#         self.BPtabWidget.SaveBlueprint()

#     def OpenBlueprint(self):
#         self.BPtabWidget.OpenBlueprint()





class CBlueprintView(QtWidgets.QTabWidget):
    m_Filter = "*.xh"

    def __init__(self, parent=None):
        super(CBlueprintView, self).__init__(parent)
        self.setMovable(True)
        self.m_PathList = []    # 存放的路径
        self.m_ListBP = []      # 存放的蓝图对象

    def AddBlueprint(self, sPath=None):
        if sPath:
            bpID = interface.OpenBlueprint(sPath)
            bpView = view.CBlueprintView(bpID)
            sTabTitle = os.path.split(sPath)[1]
            tabIndex = self.addTab(bpView, sTabTitle)
            self.setTabToolTip(tabIndex, sPath)
        else:
            bpID = interface.NewBlueprint()
            bpView = view.CBlueprintView(bpID)
            sTabTitle = "蓝图%s" % bpID
            tabIndex = self.addTab(bpView, sTabTitle)

        self.setCurrentIndex(tabIndex)
        self.m_ListBP.append(bpView)
        self.m_PathList.append(sPath)

        btn = QtWidgets.QPushButton("x")
        btn.setFlat(True)
        btn.setMaximumSize(16, 16)
        btn.clicked.connect(self.S_CloseTab)
        self.tabBar().setTabButton(tabIndex, QtWidgets.QTabBar.RightSide, btn)

    def OpenBlueprint(self):
        sPath = QtWidgets.QFileDialog.getOpenFileName(self, "打开蓝图", filter=self.m_Filter)[0]
        if sPath:
            self.AddBlueprint(sPath)

    def SaveBlueprint(self):
        iIndex = self.currentIndex()
        sPath = self.m_PathList[iIndex]
        if not sPath:
            sPath = QtWidgets.QFileDialog.getSaveFileName(self, "保存蓝图", filter=self.m_Filter)[0]
            if not sPath:
                return
        bpID = self.GetBPID(iIndex)
        interface.SaveBlueprint(bpID, sPath)

        sTabTitle = os.path.split(sPath)[1]
        self.setTabText(iIndex, sTabTitle)
        self.setTabToolTip(iIndex, sPath)

    def GetBPID(self, iIndex=None):
        if not iIndex:
            iIndex = self.currentIndex()
        oView = self.m_ListBP[iIndex]
        return oView.GetBPID()

    def Delete(self, iIndex=None):
        if iIndex is None:
            iIndex = self.currentIndex()
        if iIndex < len(self.m_PathList):
            del self.m_PathList[iIndex]
        if iIndex < len(self.m_ListBP):
            del self.m_ListBP[iIndex]

    def S_CloseTab(self):
        iIndex = self.currentIndex()
        self.Delete(iIndex)
        self.removeTab(iIndex)
        self.setCurrentIndex(self.count() - 1)
