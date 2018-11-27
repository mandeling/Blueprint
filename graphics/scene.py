# -*- coding:utf-8 -*-
"""
@Author: xiaohao
@Date: 2018-11-21 14:47:43
@Desc: 蓝图场景
"""


import weakref

from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtGui import QTransform, QCursor
from . import chartui, slotui
from .bluechartmgr import GetBlueChartMgr


class CBlueprintScene(QGraphicsScene):
    def __init__(self, parent=None):
        super(CBlueprintScene, self).__init__(parent)
        self.m_ChartInfo = {}
        self.m_SlotInfo = {}
        self.m_IsDrawLine = False
        self.m_TempPinLine = None  # 临时引脚线
        self.m_View = weakref.ref(parent)
        self.Init()

    def Init(self):
        self.setSceneRect(-10000, -10000, 20000, 20000)  # 场景大小，传入item里面

    def mouseMoveEvent(self, event):
        super(CBlueprintScene, self).mouseMoveEvent(event)
        if self.m_TempPinLine:
            self.m_TempPinLine.UpdatePosition()

    def wheelEvent(self, event):
        super(CBlueprintScene, self).wheelEvent(event)
        # 吞噬信号，不再将信号返回父窗口，禁止父窗口滑动条操作
        event.accept()

    def AddChartWidget(self, idChart, sName):
        oBlueChart = GetBlueChartMgr().GetChart(idChart)
        oWidget = chartui.CBlueChartUI(oBlueChart, sName, self)
        self.m_ChartInfo[idChart] = oWidget
        self.addItem(oWidget)
        x, y = oBlueChart.GetPos()
        oWidget.setPos(x, y)

    def BeginConnect(self, oSlotUI):
        self.m_IsDrawLine = True
        self.m_TempPinLine = slotui.CPinLine()
        self.addItem(self.m_TempPinLine)
        self.m_TempPinLine.SetStartReceiver(oSlotUI)

    def EndConnect(self, event):
        sPos = event.scenePos()
        endSlotUI = self.itemAt(sPos, QTransform())
        if isinstance(endSlotUI, slotui.CSlotUI):    # 如果不是slotui
            startSlotUI = self.m_TempPinLine.GetStartSlotUI()
            if startSlotUI.CanConnect(endSlotUI) and endSlotUI.CanConnect(startSlotUI):
                if startSlotUI.IsInputSlotUI():
                    inputSlotUI, outputSlotUI = startSlotUI, endSlotUI
                else:
                    inputSlotUI, outputSlotUI = endSlotUI, startSlotUI
                # 断开输入槽原有连线
                self.DelConnectBySlotUI(inputSlotUI)
                self.AddConnect(inputSlotUI, outputSlotUI)

        self.removeItem(self.m_TempPinLine)
        self.m_TempPinLine = None
        self.m_IsDrawLine = False

    def DelConnectBySlotUI(self, oSlotUI):
        line = oSlotUI.GetPinLine()
        self.DelConnect(line)

    def DelConnect(self, line):
        if not line:
            return
        inputSlotUI = line.GetStartSlotUI()
        inputSlotUI.SetPinLine(None)
        outputSlotUI = line.GetEndSlotUI()
        outputSlotUI.DelPinLine(line)
        self.removeItem(line)

    def AddConnect(self, inputSlotUI, outputSlotUI):
        """真正执行添加连接线"""
        line = slotui.CPinLine()
        self.addItem(line)  # 这个顺序不能变
        line.SetStartReceiver(inputSlotUI)
        line.SetEndReceiver(outputSlotUI)
        inputSlotUI.SetPinLine(line)
        outputSlotUI.AddPinLine(line)

    def GetMouseScenePos(self):
        view = self.views()[0]
        viewPos = view.mapFromGlobal(QCursor.pos())
        scenePos = view.mapToScene(viewPos)
        return scenePos
