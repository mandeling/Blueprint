# -*- coding:utf-8 -*-
"""
@Author: xiaohao
@Date: 2018-11-21 14:47:43
@Desc: 蓝图场景
"""


from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtGui import QTransform, QCursor, QPolygonF
from PyQt5.QtCore import QPointF

from PyQt5 import QtWidgets, QtCore, QtGui

from . import nodeui, pinui, lineui, uimgr, statusmgr
from editdata import interface


class CBlueprintScene(QGraphicsScene):
    def __init__(self, bpID, parent=None):
        super(CBlueprintScene, self).__init__(parent)
        self.m_BPID = bpID
        self.m_NodeUIInfo = {}
        self.m_PinInfo = {}
        self.m_IsDrawLine = False
        self.m_TempPinLine = None   # 临时引脚线
        self.m_SelectPin = None
        self.Init()

    def Init(self):
        rect = QtCore.QRectF(-10000, -10000, 20000, 20000)
        self.setSceneRect(rect)  # 场景大小，传入item里面

        # brush = QtGui.QBrush()
        # brush.setColor(QtGui.QColor(QtCore.Qt.darkGray))  # 线的颜色
        # brush.setStyle(QtCore.Qt.CrossPattern)
        # self.setBackgroundBrush(brush)
        # fillColor = QtGui.QColor(QtCore.Qt.black)   # 背景填充色
        # i = self.addRect(rect, QtCore.Qt.blue, fillColor)
        # i.setZValue(-1000)
        # # ---------------------边框颜色
        # i = self.addRect(rect, QtCore.Qt.yellow, brush)
        # i.setZValue(-1000)

    def GetBPID(self):
        return self.m_BPID

    def SetSelectPin(self, nodeID, pinID):
        self.m_SelectPin = (nodeID, pinID)

    def mouseMoveEvent(self, event):
        super(CBlueprintScene, self).mouseMoveEvent(event)
        if self.m_TempPinLine:
            self.m_TempPinLine.UpdatePosition()

    def wheelEvent(self, event):
        super(CBlueprintScene, self).wheelEvent(event)
        # 吞噬信号，不再将信号返回父窗口，禁止父窗口滑动条操作
        event.accept()

    def SetNodeMove(self, offpos):
        for nodeID in statusmgr.GetStatusMgr().GetSelectNode(self.m_BPID):
            oNodeUI = uimgr.GetUIMgr().GetNodeUI(self.m_BPID, nodeID)
            oNodeUI.SetMouseMovePos(offpos)

    def AddNodeUI(self, nodeID, tPos):
        oWidget = nodeui.CNodeUI(self.m_BPID, nodeID)
        self.m_NodeUIInfo[nodeID] = oWidget
        self.addItem(oWidget)
        x, y = tPos
        oWidget.setPos(x, y)

    def DelNodeUI(self, nodeID):
        oWidget = self.m_NodeUIInfo.get(nodeID, None)
        if not oWidget:
            return
        self.removeItem(oWidget)
        del self.m_NodeUIInfo[nodeID]

    def BeginConnect(self, startPinUI):
        self.m_IsDrawLine = True
        self.m_TempPinLine = lineui.CLineUI(self.m_BPID)
        self.addItem(self.m_TempPinLine)
        self.m_TempPinLine.SetStartReceiver(startPinUI)

    def EndConnect(self, event):
        sPos = event.scenePos()
        endPinUI = self.itemAt(sPos, QTransform())
        if isinstance(endPinUI, pinui.CPinUI):    # 如果是pinui
            startPinUI = self.m_TempPinLine.GetStartPinUI()
            bpID, sNodeID, sPinID = startPinUI.GetIDInfo()
            bpID, eNodeID, ePinID = endPinUI.GetIDInfo()
            if interface.PinCanConnect(bpID, sNodeID, sPinID, eNodeID, ePinID):
                if interface.IsInputPin(bpID, sNodeID, sPinID):
                    inputPinUI, outputPinUI = startPinUI, endPinUI
                else:
                    inputPinUI, outputPinUI = endPinUI, startPinUI
                self.OnAddConnect(inputPinUI, outputPinUI)

        self.removeItem(self.m_TempPinLine)
        self.m_TempPinLine = None
        self.m_IsDrawLine = False
        self.m_SelectPin = None

    def DelConnect(self, lineID):
        oLineUI = uimgr.GetUIMgr().GetLineUI(self.m_BPID, lineID)
        interface.DelLine(self.m_BPID, lineID)
        self.removeItem(oLineUI)

    def OnAddConnect(self, inputPinUI, outputPinUI):
        bpID, iNodeID, iPinID = inputPinUI.GetIDInfo()
        bpID, oNodeID, oPinID = outputPinUI.GetIDInfo()
        lineID = interface.AddLine(bpID, oNodeID, oPinID, iNodeID, iPinID)
        self.AddConnect(lineID, inputPinUI, outputPinUI)

    def AddConnect(self, lineID, inputPinUI, outputPinUI):
        """真正执行添加连接线"""
        line = lineui.CLineUI(self.m_BPID, lineID)
        self.addItem(line)  # 这个顺序不能变
        line.SetStartReceiver(inputPinUI)
        line.SetEndReceiver(outputPinUI)

    def GetMouseScenePos(self):
        view = self.views()[0]
        viewPos = view.mapFromGlobal(QCursor.pos())
        scenePos = view.mapToScene(viewPos)
        return scenePos
