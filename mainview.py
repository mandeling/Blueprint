# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2019-01-08 15:28:00
@Desc: 主界面
"""

from PyQt5.QtWidgets import QMainWindow, QDockWidget, QSizePolicy, QWidget
from PyQt5.QtCore import Qt

from pubcode.pubqt.pubmenu import menumgr, menudefine
from editdata import interface
from signalmgr import GetSignal


class CMainView(QMainWindow):
    def __init__(self, parent=None):
        super(CMainView, self).__init__(parent)
        self._InitMenu()
        self._InitCorner()
        self._InitDock()

    def _InitMenu(self):
        menumgr.InitMgr(self)
        oMenuMgr = menumgr.GetMenuMgr()
        for dMenuConfig in self.GetMenunInfo():
            oMenuMgr.AddMenu(dMenuConfig)
        pMenuBar = oMenuMgr.BuildChildMenu()
        self.setMenuBar(pMenuBar)

    def _InitCorner(self):
        self.setCorner(Qt.TopLeftCorner, Qt.LeftDockWidgetArea)
        self.setCorner(Qt.BottomLeftCorner, Qt.LeftDockWidgetArea)
        self.setCorner(Qt.TopRightCorner, Qt.RightDockWidgetArea)
        self.setCorner(Qt.BottomRightCorner, Qt.RightDockWidgetArea)

    def _InitDock(self):
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        topDock = QDockWidget("顶部面板", self)
        topDock.setSizePolicy(sizePolicy)
        topDock.setObjectName("topDock")
        topDock.setWidget(CWidget("顶部面板"))

        bottomDock = QDockWidget("底部面板", self)
        bottomDock.setSizePolicy(sizePolicy)
        bottomDock.setObjectName("bottomDock")
        bottomDock.setWidget(CWidget("底部面板"))

        leftDock = QDockWidget("左侧面板", self)
        leftDock.setSizePolicy(sizePolicy)
        leftDock.setObjectName("leftDock")
        leftDock.setWidget(CWidget("左侧面板"))

        rightDock = QDockWidget("右侧面板", self)
        rightDock.setSizePolicy(sizePolicy)
        rightDock.setObjectName("rightDock")
        rightDock.setWidget(CWidget("右侧面板"))

        self.addDockWidget(Qt.RightDockWidgetArea, rightDock)
        self.addDockWidget(Qt.TopDockWidgetArea, topDock)
        self.addDockWidget(Qt.BottomDockWidgetArea, bottomDock)
        self.addDockWidget(Qt.LeftDockWidgetArea, leftDock)
        self.setCentralWidget(CWidget("中心界面"))

    def GetMenunInfo(self):
        return [
            {
                menudefine.MENU_NAME: "文件/新建蓝图",
                menudefine.MENU_FUNCTION_NAME: self.S_NewBlueprint,
                menudefine.MENU_SHORTCUT_NAME: "Ctrl+N"
            },
            {
                menudefine.MENU_NAME: "文件/保存所有蓝图",
                menudefine.MENU_FUNCTION_NAME: self.S_SaveAllBlueprint,
                menudefine.MENU_SHORTCUT_NAME: "Ctrl+S"
            },
            {
                menudefine.MENU_NAME: "文件/打开蓝图",
                menudefine.MENU_FUNCTION_NAME: self.S_OpenBlueprint,
                menudefine.MENU_SHORTCUT_NAME: "Ctrl+O"
            },
        ]

    def S_NewBlueprint(self):
        bpID = interface.NewBlueprint()
        GetSignal().UI_NEW_BLUEPRINT.emit(bpID)

    def S_SaveAllBlueprint(self):
        pass

    def S_OpenBlueprint(self):
        GetSignal().UI_OPEN_BLUEPRINT.emit()


class CWidget(QWidget):
    def __init__(self, sName, parent=None):
        super(CWidget, self).__init__(parent)
        self.setWindowTitle(sName)
