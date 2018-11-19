# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-11-09 09:55:45
@Desc: 
"""

import weakref

from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtGui import QTransform
from PyQt5.QtCore import Qt
from . import chartui
from .bluechartmgr import GetBlueChartMgr


class CBlueprintScene(QGraphicsScene):
    def __init__(self, parent=None):
        super(CBlueprintScene, self).__init__(parent)
        self.m_ChartInfo = {}
        self.m_SlotInfo = {}
        self.m_Pos = None   # 创建图表的位置,已换算成对于场景的位置
        self.m_LeftBtnStartPos = None
        self.m_View = weakref.ref(parent)
        self.Init()
        self.InitSignal()

    def Init(self):
        self.setSceneRect(-10000, -10000, 20000, 20000)  # 场景大小，传入item里面

    def InitSignal(self):
        pass

    def mousePressEvent(self, event):
        super(CBlueprintScene, self).mousePressEvent(event)
        if event.isAccepted():
            return
        sPos = event.scenePos()
        if self.itemAt(sPos, QTransform()):
            return
        if event.button() == Qt.LeftButton or event.button() == Qt.RightButton:
            GetBlueChartMgr().ClearSelect()
        if event.button() == Qt.LeftButton:
            self.m_LeftBtnStartPos = sPos

    def mouseMoveEvent(self, event):
        super(CBlueprintScene, self).mouseMoveEvent(event)
        if not self.m_LeftBtnStartPos:
            return

    def mouseReleaseEvent(self, event):
        super(CBlueprintScene, self).mouseReleaseEvent(event)

    def wheelEvent(self, event):
        super(CBlueprintScene, self).wheelEvent(event)
        # 吞噬信号，不再将信号返回父窗口，禁止父窗口滑动条操作
        event.accept()

    def SetPos(self, pos):
        self.m_Pos = pos

    def AddChartWidget(self, idChart, sName):
        oBlueChart = GetBlueChartMgr().GetChart(idChart)
        oWidget = chartui.CBlueChartUI(oBlueChart, sName, self)
        self.m_ChartInfo[idChart] = oWidget
        self.addItem(oWidget)
        x, y = oBlueChart.GetPos()
        oWidget.setPos(x, y)
        # oWidget.setPos(self.m_Pos.x(), self.m_Pos.y())
