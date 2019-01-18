# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-11-30 13:58:24
@Desc: 主窗口
"""

from PyQt5.QtWidgets import QMainWindow, QDockWidget, QSizePolicy, QMenuBar, QAction
from PyQt5.QtCore import Qt

from bpwidget import graphictab
from bpwidget import detailui, menuui, bpattrwidget, searchui
from pubcode.pubqt.pubmenu import menumgr, menudefine
from mainwidget import logwidget


class CBlueprintView(QMainWindow):
    def __init__(self, bpID, parent=None):
        super(CBlueprintView, self).__init__(parent)
        self.m_BPID = bpID
        self.m_BPTabWidget = graphictab.CBPTabWidget(bpID, self)
        self.m_BPAttrWidget = bpattrwidget.CBPAttrWidget(bpID, self)
        self.m_DeltailWidget = detailui.CDetailUI(bpID, self)
        self.m_MenuWidget = menuui.CMenuUI(bpID, self)
        self.m_SearchWidget = searchui.CSearchWidget(bpID, self)
        self.m_LogWidget = logwidget.GetLogWidget()
        self._InitCorner()
        self._InitDock()
        self._InitMenu()
        self._InitWindowsMenu()

    def _InitCorner(self):
        self.setCorner(Qt.TopLeftCorner, Qt.LeftDockWidgetArea)
        self.setCorner(Qt.BottomLeftCorner, Qt.LeftDockWidgetArea)
        self.setCorner(Qt.TopRightCorner, Qt.RightDockWidgetArea)
        self.setCorner(Qt.BottomRightCorner, Qt.RightDockWidgetArea)

    def _InitDock(self):
        # self.setDockNestingEnabled(True)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        topDock = QDockWidget("菜单", self)
        topDock.setSizePolicy(sizePolicy)
        topDock.setObjectName("topDock")
        topDock.setWidget(self.m_MenuWidget)

        bottomDock = QDockWidget("搜索", self)
        bottomDock.setSizePolicy(sizePolicy)
        bottomDock.setObjectName("bottomDock")
        bottomDock.setWidget(self.m_SearchWidget)

        leftDock = QDockWidget("属性", self)
        leftDock.setSizePolicy(sizePolicy)
        leftDock.setObjectName("leftDock")
        leftDock.setWidget(self.m_BPAttrWidget)

        rightDock = QDockWidget("细节", self)
        rightDock.setSizePolicy(sizePolicy)
        rightDock.setObjectName("rightDock")
        rightDock.setWidget(self.m_DeltailWidget)

        logDock = QDockWidget("日志面板", self)
        logDock.setSizePolicy(sizePolicy)
        logDock.setObjectName("logDock")
        logDock.setWidget(self.m_LogWidget)

        self.addDockWidget(Qt.RightDockWidgetArea, rightDock)
        self.addDockWidget(Qt.TopDockWidgetArea, topDock)
        self.addDockWidget(Qt.BottomDockWidgetArea, bottomDock)
        self.addDockWidget(Qt.BottomDockWidgetArea, logDock)
        self.tabifyDockWidget(bottomDock, logDock)
        logDock.raise_()

        self.addDockWidget(Qt.LeftDockWidgetArea, leftDock)
        self.setCentralWidget(self.m_BPTabWidget)

    def _InitMenu(self):
        oMenu = menumgr.InitMenu(self)
        for dMenuConfig in self.GetMenunInfo():
            oMenu.AddMenu(dMenuConfig)
        pMenuBar = oMenu.BuildChildMenu()
        self.setMenuBar(pMenuBar)

    def _InitWindowsMenu(self):
        def UpdateWindowsStatue():
            dMap = {oAction.text(): oAction for oAction in oWindowsMenu.actions()}
            for oChild in lstChilde:
                dMap[oChild.windowTitle()].setChecked(oChild.isVisible())

        def OnWindows():
            for oChild in lstChilde:
                oSender = self.sender()
                if oSender.text() != oChild.windowTitle():
                    continue
                if oSender.isChecked():
                    oChild.show()
                else:
                    oChild.hide()
                return

        oMenu = menumgr.GetMenu(self)
        oWindowsMenu = oMenu.GetSubMenu("窗口")
        oWindowsMenu.aboutToShow.connect(UpdateWindowsStatue)
        oWindowsMenu.clear()

        lstChilde = []
        for oChild in self.children():
            if not isinstance(oChild, (QDockWidget,)):
                continue
            lstChilde.append(oChild)

        for oChild in lstChilde:
            oAction = QAction(oChild.windowTitle(), self)
            oAction.triggered.connect(OnWindows)
            oAction.setCheckable(True)
            oWindowsMenu.addAction(oAction)

    def GetMenunInfo(self):
        return [
            {
                menudefine.MENU_NAME: "窗口/",
            }
        ]
