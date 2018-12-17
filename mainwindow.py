# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-11-30 13:58:24
@Desc: 主窗口
"""

from PyQt5 import QtWidgets, QtCore
from menu import menumgr, menudefine
from graphics import bpwidget
from bpwidget import detailui, variableui


class CMainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(CMainWindow, self).__init__(parent)
        self.m_BlutprintWidget = bpwidget.CBlueprintWidget(self)
        self.m_VariableWidget = variableui.CVariableWidget(self)
        self.m_DeltailWidget = detailui.CDetailUI(self)
        self.InitUI()
        self.InitView()

    def InitUI(self):
        self.showMaximized()
        self.setGeometry(300, 150, 1200, 800)
        self.setWindowTitle("蓝图")

    def InitView(self):
        self.InitMenu()
        self.InitCorner()
        self.InitDock()
        self.InitCenter()

    def InitMenu(self):
        menumgr.InitMgr(self)
        oMenuMgr = menumgr.GetMenuMgr()
        for dMenuConfig in self.GetMenunInfo():
            oMenuMgr.AddMenu(dMenuConfig)
        pMenuBar = oMenuMgr.BuildChildMenu()
        self.setMenuBar(pMenuBar)

    def InitCorner(self):
        self.setCorner(QtCore.Qt.TopLeftCorner, QtCore.Qt.LeftDockWidgetArea)
        self.setCorner(QtCore.Qt.BottomLeftCorner, QtCore.Qt.BottomDockWidgetArea)
        self.setCorner(QtCore.Qt.TopRightCorner, QtCore.Qt.RightDockWidgetArea)
        self.setCorner(QtCore.Qt.BottomRightCorner, QtCore.Qt.RightDockWidgetArea)

    def InitDock(self):
        # self.setDockNestingEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)

        leftDock = QtWidgets.QDockWidget("左侧面板", self)
        leftDock.setSizePolicy(sizePolicy)
        leftDock.setObjectName("leftDock")
        leftDock.setWidget(self.m_VariableWidget)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, leftDock)

        # rightDock = QtWidgets.QDockWidget("右侧面板", self)
        # rightDock.setSizePolicy(sizePolicy)
        # rightDock.setObjectName("m_RightDockt")
        # self.addDockWidget(QtCore.Qt.RightDockWidgetArea, rightDock)

        # downDock = QtWidgets.QDockWidget("底部面板", self)
        # downDock.setSizePolicy(sizePolicy)
        # downDock.setObjectName("m_DownDockt")
        # self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, downDock)

        detailDock = QtWidgets.QDockWidget("细节", self)
        detailDock.setSizePolicy(sizePolicy)
        detailDock.setObjectName("detailDock")
        detailDock.setWidget(self.m_DeltailWidget)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, detailDock)

        blueprintDock = QtWidgets.QDockWidget("蓝图", self)
        blueprintDock.setSizePolicy(sizePolicy)
        blueprintDock.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        blueprintDock.setObjectName("blueprintDock")
        blueprintDock.setWidget(self.m_BlutprintWidget)
        self.addDockWidget(QtCore.Qt.TopDockWidgetArea, blueprintDock)

        self.splitDockWidget(leftDock, blueprintDock, QtCore.Qt.Horizontal)
        self.splitDockWidget(blueprintDock, detailDock, QtCore.Qt.Horizontal)

    def InitCenter(self):
        pass

    def GetMenunInfo(self):
        return [
            {
                menudefine.MENU_NAME: "文件/新建蓝图",
                menudefine.MENU_FUNCTION_NAME: self.m_BlutprintWidget.NewBlueprint,
                menudefine.MENU_SHORTCUT_NAME: "Ctrl+N"
            },
            {
                menudefine.MENU_NAME: "文件/保存蓝图",
                menudefine.MENU_FUNCTION_NAME: self.m_BlutprintWidget.SaveBlueprint,
                menudefine.MENU_SHORTCUT_NAME: "Ctrl+S"
            },
            {
                menudefine.MENU_NAME: "文件/打开蓝图",
                menudefine.MENU_FUNCTION_NAME: self.m_BlutprintWidget.OpenBlueprint,
                menudefine.MENU_SHORTCUT_NAME: "Ctrl+O"
            },
        ]
