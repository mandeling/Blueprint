# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-11-30 13:58:24
@Desc: 主窗口
"""

from PyQt5.QtWidgets import QMainWindow, QStyleFactory,\
    QWidget, QDockWidget, QSizePolicy, QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor

from menu import menumgr, menudefine
from graphics import bpwidget
from bpwidget import detailui, variableui


class CMainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(CMainWindow, self).__init__(parent)
        self.m_BlutprintWidget = bpwidget.CBlueprintWidget(self)
        self.m_VariableWidget = variableui.CVariableWidget(self)
        self.m_DeltailWidget = detailui.CDetailUI(self)
        self.m_MenuWidget = None
        self.m_LogWidget = None
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

    def InitMenu(self):
        menumgr.InitMgr(self)
        oMenuMgr = menumgr.GetMenuMgr()
        for dMenuConfig in self.GetMenunInfo():
            oMenuMgr.AddMenu(dMenuConfig)
        pMenuBar = oMenuMgr.BuildChildMenu()
        self.setMenuBar(pMenuBar)

    def InitCorner(self):
        self.setCorner(Qt.TopLeftCorner, Qt.LeftDockWidgetArea)
        self.setCorner(Qt.BottomLeftCorner, Qt.LeftDockWidgetArea)
        self.setCorner(Qt.TopRightCorner, Qt.RightDockWidgetArea)
        self.setCorner(Qt.BottomRightCorner, Qt.RightDockWidgetArea)

    def InitDock(self):
        # self.setDockNestingEnabled(True)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        topDock = QDockWidget("菜单", self)
        topDock.setSizePolicy(sizePolicy)
        topDock.setObjectName("topDock")
        topDock.setWidget(self.m_MenuWidget)

        bottomDock = QDockWidget("Log面板", self)
        bottomDock.setSizePolicy(sizePolicy)
        bottomDock.setObjectName("bottomDock")
        bottomDock.setWidget(self.m_LogWidget)

        leftDock = QDockWidget("变量", self)
        leftDock.setSizePolicy(sizePolicy)
        leftDock.setObjectName("leftDock")
        leftDock.setWidget(self.m_VariableWidget)

        rightDock = QDockWidget("细节", self)
        rightDock.setSizePolicy(sizePolicy)
        rightDock.setObjectName("rightDock")
        rightDock.setWidget(self.m_DeltailWidget)

        self.addDockWidget(Qt.RightDockWidgetArea, rightDock)
        self.addDockWidget(Qt.TopDockWidgetArea, topDock)
        self.addDockWidget(Qt.BottomDockWidgetArea, bottomDock)
        self.addDockWidget(Qt.LeftDockWidgetArea, leftDock)
        self.setCentralWidget(self.m_BlutprintWidget)

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
