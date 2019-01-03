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
from signalmgr import GetSignal


class CBlueprintScene(QGraphicsScene):
    def __init__(self, bpID, parent=None):
        super(CBlueprintScene, self).__init__(parent)
        self.m_BPID = bpID
        self.m_PinInfo = {}
        self.m_IsDrawLine = False
        self.m_TempPinLine = None   # 临时引脚连线
        self._Init()
        self._InitSignal()

    def _Init(self):
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

    def _InitSignal(self):
        GetSignal().DEL_LINE.emit(self.S_DelLineUI)

    def GetBPID(self):
        return self.m_BPID

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
            oNodeUI = uimgr.GetUIMgr().GetNodeUI(nodeID)
            oNodeUI.SetMouseMovePos(offpos)

    def AddNodeUI(self, nodeID, tPos):
        oNodeUI = nodeui.CNodeUI(nodeID)
        self.addItem(oNodeUI)
        x, y = tPos
        oNodeUI.setPos(x, y)

    def DelNodeUI(self, nodeID):
        oNodeUI = uimgr.GetUIMgr().GetNodeUI(nodeID)
        if not oNodeUI:
            return
        self.removeItem(oNodeUI)
        # TODO

    def BeginConnect(self, startPinID):
        self.m_IsDrawLine = True
        self.m_TempPinLine = lineui.CLineUI()
        self.addItem(self.m_TempPinLine)
        self.m_TempPinLine.SetStartPinID(startPinID)

    def EndConnect(self, event):
        sPos = event.scenePos()
        endPinUI = self.itemAt(sPos, QTransform())
        if isinstance(endPinUI, pinui.CPinUI):    # 如果是pinui
            sPinID = self.m_TempPinLine.GetStartPinID()
            ePinID = endPinUI.GetPID()
            if interface.PinCanConnect(sPinID, ePinID):
                if interface.IsInputPin(sPinID):
                    inputPinID, outputPinID = sPinID, ePinID
                else:
                    inputPinID, outputPinID = ePinID, sPinID
                self.OnAddConnect(inputPinID, outputPinID)

        self.removeItem(self.m_TempPinLine)
        self.m_TempPinLine = None
        self.m_IsDrawLine = False

    def DelConnect(self, lineID):
        interface.DelLine(lineID)
        self.S_DelLineUI(lineID)

    def S_DelLineUI(self, lineID):
        oLineUI = uimgr.GetUIMgr().GetLineUI(lineID)
        self.removeItem(oLineUI)

    def OnAddConnect(self, inputPinID, outputPinID):
        """真正执行添加连接线"""
        lineID = interface.AddLine(self.m_BPID, outputPinID, inputPinID)
        line = lineui.CLineUI(lineID)
        self.addItem(line)
        line.SetStartPinID(outputPinID)
        line.SetEndPinID(inputPinID)

    def GetMouseScenePos(self):
        view = self.views()[0]
        viewPos = view.mapFromGlobal(QCursor.pos())
        scenePos = view.mapToScene(viewPos)
        return scenePos
