# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-11-09 09:55:45
@Desc: 
"""

from . import chartui
from .manager import GetBlueChartMgr

from PyQt5.QtWidgets import QGraphicsScene


class CBlueprintScene(QGraphicsScene):
    def __init__(self, parent=None):
        super(CBlueprintScene, self).__init__(parent)
        self.m_ChartInfo = {}
        self.m_Pos = None   # 创建图表的位置,已换算成对于场景的位置
        self.Init()
        self.InitSignal()

    def Init(self):
        self.setSceneRect(-10000, -10000, 20000, 20000)  # 场景大小，传入item里面

    def InitSignal(self):
        GetBlueChartMgr().SIG_ADD_CHART.connect(self.S_AddChartWidget)

    def wheelEvent(self, event):
        super(CBlueprintScene, self).wheelEvent(event)
        # 吞噬信号，不再将信号返回父窗口，禁止父窗口滑动条操作
        event.accept()

    def SetPos(self, pos):
        self.m_Pos = pos

    def S_AddChartWidget(self, iID):
        oBlueChart = GetBlueChartMgr().GetChart(iID)
        oWidget = chartui.CBlueChartUI(oBlueChart, self)
        self.m_ChartInfo[iID] = oWidget
        self.addItem(oWidget)
        x, y = oBlueChart.GetPos()
        oWidget.setPos(x, y)
        # oWidget.setPos(self.m_Pos.x(), self.m_Pos.y())
