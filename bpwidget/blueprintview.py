# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-11-30 13:58:24
@Desc: 主窗口
"""

from PyQt5.QtWidgets import QMainWindow, QDockWidget, QSizePolicy
from PyQt5.QtCore import Qt

from bpwidget import graphictab
from bpwidget import detailui, menuui, bpattrwidget, searchui


class CBlueprintView(QMainWindow):
    def __init__(self, bpID, parent=None):
        super(CBlueprintView, self).__init__(parent)
        self.m_BPID = bpID
        self.m_BPTabWidget = graphictab.CBPTabWidget(bpID, self)
        self.m_BPAttrWidget = bpattrwidget.CBPAttrWidget(bpID, self)
        self.m_DeltailWidget = detailui.CDetailUI(bpID, self)
        self.m_MenuWidget = menuui.CMenuUI(bpID, self)
        self.m_SearchWidget = searchui.CSearchWidget(bpID, self)
        self.m_LogWidget = None
        self._InitCorner()
        self._InitDock()

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

        self.addDockWidget(Qt.RightDockWidgetArea, rightDock)
        self.addDockWidget(Qt.TopDockWidgetArea, topDock)
        self.addDockWidget(Qt.BottomDockWidgetArea, bottomDock)
        self.addDockWidget(Qt.LeftDockWidgetArea, leftDock)
        self.setCentralWidget(self.m_BPTabWidget)
