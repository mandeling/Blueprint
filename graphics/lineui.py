# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-12-11 09:50:23
@Desc: 引脚连线UI
"""


from PyQt5.QtWidgets import QGraphicsPathItem, QStyle
from PyQt5.QtGui import QCursor, QPainterPath, QPainter, QPen
from PyQt5.QtCore import QPointF, Qt

from viewmgr.uimgr import GetUIMgr
from editdata import interface


class CLineUI(QGraphicsPathItem):
    """引脚连线"""

    def __init__(self, lineID=-1, parent=None):
        super(CLineUI, self).__init__(parent)
        self.m_LineID = lineID
        self.setZValue(-1)
        self.m_StartPinID = None
        self.m_EndPinID = None
        self.m_StartPoint = None
        self.m_EndPoint = None
        self.m_PenColor = Qt.white
        self.m_BakColor = Qt.white
        self._InitUI()
        if lineID != -1:    # -1为临时连线
            GetUIMgr().AddLineUI(lineID, self)

    def __del__(self):
        if self.m_LineID == -1:
            return
        GetUIMgr().DelLineUI(self.m_LineID)

    def _InitUI(self):
        self.setFlag(QGraphicsPathItem.ItemIsSelectable)
        self.RecalculateShapeAndBount()
        self._SetPen()
        self.setZValue(-1)
        self.update()

    def RecalculateShapeAndBount(self):
        if self.m_StartPoint is None or self.m_EndPoint is None:
            qPath = QPainterPath()
            qPath.addRect(0, 0, 0, 0)
            return
        if self.m_StartPoint.x() < self.m_EndPoint.x():
            centerY = (self.m_StartPoint.y() + self.m_EndPoint.y()) // 2
            c1 = QPointF(self.m_StartPoint.x(), centerY)
            c2 = QPointF(self.m_EndPoint.x(), centerY)
        else:
            centerX = (self.m_StartPoint.x() + self.m_EndPoint.x()) // 2
            c1 = QPointF(centerX, self.m_StartPoint.y())
            c2 = QPointF(centerX, self.m_EndPoint.y())
        qPath = QPainterPath()
        qPath.moveTo(self.m_StartPoint)
        qPath.cubicTo(c1, c2, self.m_EndPoint)
        qPath.addEllipse(self.m_StartPoint, 4, 4)
        qPath.addEllipse(self.m_EndPoint, 4, 4)
        self.setPath(qPath)

    def _SetPen(self):
        pen = QPen(self.m_PenColor)
        pen.setWidth(2)
        pen.setJoinStyle(Qt.MiterJoin)
        self.setPen(pen)

    def SetStartPinID(self, pinID):
        if interface.IsFlowPin(pinID):
            self.m_PenColor = Qt.blue
            self._SetPen()
        self.m_StartPinID = pinID
        self.UpdatePosition()

    def GetStartPinID(self):
        return self.m_StartPinID

    def SetEndPinID(self, pinID):
        self.m_EndPinID = pinID
        self.UpdatePosition()

    def UpdatePosition(self):
        startPinUI = GetUIMgr().GetPinBtnUI(self.m_StartPinID)
        nodeID = interface.GetNodeIDByPinID(self.m_StartPinID)
        nodeUI = GetUIMgr().GetNodeUI(nodeID)
        if startPinUI:
            self.m_StartPoint = startPinUI.GetScenePos()
        if self.m_EndPinID:
            endPinUI = GetUIMgr().GetPinBtnUI(self.m_EndPinID)
            self.m_EndPoint = endPinUI.GetScenePos()
        else:
            self.m_EndPoint = nodeUI.scene().GetMouseScenePos(QCursor.pos())
        self.prepareGeometryChange()
        self.RecalculateShapeAndBount()

    def paint(self, painter, option, widget=None):
        painter.setRenderHint(QPainter.Antialiasing, True)
        option.state = QStyle.State_None
        super(CLineUI, self).paint(painter, option, widget)

    def SetRunColor(self):
        self.m_BakColor = self.m_PenColor
        self.m_PenColor = Qt.red
        self._SetPen()

    def SetStopColor(self):
        self.m_PenColor = self.m_BakColor
        self._SetPen()
