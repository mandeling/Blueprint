# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-11-30 13:58:24
@Desc: 主窗口
"""

from PyQt5 import QtWidgets, QtCore
from menu import menumgr, menudefine


class CMainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(CMainWindow, self).__init__(parent)
        self.InitUI()
        self.InitView()

    def InitUI(self):
        self.showMaximized()
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
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)

        leftDock = QtWidgets.QDockWidget("左侧面板", self)
        leftDock.setSizePolicy(sizePolicy)
        leftDock.setObjectName("m_LeftDockt")
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, leftDock)

        # rightDock = QtWidgets.QDockWidget("右侧面板", self)
        # rightDock.setSizePolicy(sizePolicy)
        # rightDock.setObjectName("m_RightDockt")
        # self.addDockWidget(QtCore.Qt.RightDockWidgetArea, rightDock)

        blueprintDock = QtWidgets.QDockWidget("蓝图", self)
        blueprintDock.setSizePolicy(sizePolicy)
        blueprintDock.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        blueprintDock.setObjectName("m_BlueprintDockt")
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, blueprintDock)

        downDock = QtWidgets.QDockWidget("底部面板", self)
        downDock.setSizePolicy(sizePolicy)
        downDock.setObjectName("m_DownDockt")
        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, downDock)

    def InitCenter(self):
        pass

    def GetMenunInfo(self):
        return [
            {
                menudefine.MENU_NAME: "文件/新建蓝图",
                menudefine.MENU_FUNCTION_NAME: self.NewBlueprint,
                menudefine.MENU_SHORTCUT_NAME: "Ctrl+N"
            },
            {
                menudefine.MENU_NAME: "文件/保存蓝图",
                menudefine.MENU_FUNCTION_NAME: self.SaveBlueprint,
                menudefine.MENU_SHORTCUT_NAME: "Ctrl+S"
            },
        ]

    def NewBlueprint(self):
        pass

    def SaveBlueprint(self):
        pass
