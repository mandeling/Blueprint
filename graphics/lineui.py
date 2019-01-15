# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-12-11 09:50:23
@Desc: 
"""


from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import QCursor

from viewmgr.uimgr import GetUIMgr
from editdata import interface


class CLineUI(QtWidgets.QGraphicsItem):
    """引脚连线"""

    def __init__(self, lineID=-1, parent=None):
        super(CLineUI, self).__init__(parent)
        self.m_LineID = lineID
        self.setZValue(-1)
        self.m_StartPinID = None
        self.m_EndPinID = None
        self.m_StartPoint = None
        self.m_EndPoint = None
        self.m_Path = None
        self.m_Rect = None
        self.RecalculateShapeAndBount()
        if lineID != -1:    # -1为临时连线
            GetUIMgr().AddLineUI(lineID, self)

    def __del__(self):
        if self.m_LineID == -1:
            return
        GetUIMgr().DelLineUI(self.m_LineID)

    def GetStartPinChartName(self):
        oPinUI = self.GetStartPinUI()
        sName = oPinUI.GetChartName()
        return sName

    def RecalculateShapeAndBount(self):
        if self.m_StartPoint is None or self.m_EndPoint is None:
            self.m_Path = QtGui.QPainterPath()
            self.m_Path.addRect(0, 0, 0, 0)
            self.m_Rect = self.m_Path.boundingRect()
            return
        if self.m_StartPoint.x() < self.m_EndPoint.x():
            centerY = (self.m_StartPoint.y() + self.m_EndPoint.y()) // 2
            c1 = QtCore.QPointF(self.m_StartPoint.x(), centerY)
            c2 = QtCore.QPointF(self.m_EndPoint.x(), centerY)
        else:
            centerX = (self.m_StartPoint.x() + self.m_EndPoint.x()) // 2
            c1 = QtCore.QPointF(centerX, self.m_StartPoint.y())
            c2 = QtCore.QPointF(centerX, self.m_EndPoint.y())
        self.m_Path = QtGui.QPainterPath()
        self.m_Path.moveTo(self.m_StartPoint)
        self.m_Path.cubicTo(c1, c2, self.m_EndPoint)
        self.m_Path.addEllipse(self.m_StartPoint, 4, 4)
        self.m_Path.addEllipse(self.m_EndPoint, 4, 4)
        self.m_Rect = self.m_Path.boundingRect()

    def SetStartPinID(self, pinID):
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

    def paint(self, painter, _, __):
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        painter.setPen(QtCore.Qt.white)
        painter.drawPath(self.m_Path)
