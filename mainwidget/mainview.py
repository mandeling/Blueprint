# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2019-01-08 15:28:00
@Desc: 主界面
"""

import os

from PyQt5.QtWidgets import QMainWindow, QDockWidget, QSizePolicy, QWidget
from PyQt5.QtCore import Qt

from . import filetree
from pubcode.pubqt.pubmenu import menumgr, menudefine
from editdata import interface
from signalmgr import GetSignal


class CMainView(QMainWindow):
    def __init__(self, parent=None):
        super(CMainView, self).__init__(parent)
        self.m_FileTree = filetree.CFileTree(self)
        self._InitMenu()
        self._InitCorner()
        self._InitDock()

    def _InitMenu(self):
        oMenu = menumgr.InitMenu(self)
        for dMenuConfig in self.GetMenunInfo():
            oMenu.AddMenu(dMenuConfig)
        pMenuBar = oMenu.BuildChildMenu()
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
        leftDock.setWidget(self.m_FileTree)

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

    def _GetFileName(self):
        for x in range(100):
            s = ""
            if x:
                s = str(x)
            sPath = "bpfile/blueprint%s.xh" % s
            if not os.path.exists(sPath):
                return sPath

    def S_NewBlueprint(self):
        sPath = self._GetFileName()
        bpID = interface.NewBlueprint()
        interface.SaveBlueprint(bpID, sPath)

    def S_SaveAllBlueprint(self):
        GetSignal().UI_SAVE_ALL_BLUEPRINT.emit()

    def S_OpenBlueprint(self):
        GetSignal().UI_OPEN_BLUEPRINT.emit()


class CWidget(QWidget):
    def __init__(self, sName, parent=None):
        super(CWidget, self).__init__(parent)
        self.setWindowTitle(sName)
