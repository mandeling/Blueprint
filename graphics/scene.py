# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-11-09 09:55:45
@Desc: 
"""

from . import item, chartui
from .manager import GetBlueChartMgr

from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QApplication, QMenu, QAction
from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtCore import Qt


class CBlueprintScene(QGraphicsScene):
    def __init__(self, parent=None):
        super(CBlueprintScene, self).__init__(parent)
        self.m_ChartInfo = {}
        self.m_Pos = None   # 创建图表的位置
        self.Init()
        self.InitSignal()

    def Init(self):
        self.setSceneRect(0, 0, 40, 30)  # 场景大小，传入item里面

    def InitSignal(self):
        GetBlueChartMgr().SIG_ADD_CHART.connect(self.AddChartWidget)

    # def mousePressEvent(self, event):
    #     super(CBlueprintScene, self).mousePressEvent(event)
    #     print("scene.mousePressEvent")
    #     if event.isAccepted():
    #         return
    #     if event.button() == Qt.LeftButton:
    #         point = event.scenePos()
    #         sceneRect = self.sceneRect()
    #         oItem = item.CBlueprintItem(sceneRect)
    #         oItem.setPos(point.x(), point.y())
    #         self.addItem(oItem)
    #         self.m_ItemList.append(oItem)

    def SetPos(self, pos):
        self.m_Pos = pos

    def AddChartWidget(self, iID):
        print("=" * 30)
        print(iID)
        oBlueChart = GetBlueChartMgr().GetChart(iID)
        oWidget = chartui.CBlueChartUI(oBlueChart, self)
        self.m_ChartInfo[iID] = oWidget
        self.addItem(oWidget)
        x, y = oBlueChart.GetPos()
        oWidget.setPos(x, y)
