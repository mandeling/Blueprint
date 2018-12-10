# -*- coding:utf-8 -*-
"""
@Author: xiaohao
@Date: 2018-11-21 14:52:42
@Desc: 信号槽界面UI
"""

import weakref
import miscqt
import misc

from PyQt5.QtWidgets import QGraphicsPolygonItem, QMenu, QGraphicsItem
from PyQt5.QtCore import Qt, QPointF, QRectF
from PyQt5.QtGui import QCursor, QPainterPath, QPainter, QPolygonF

from .slotmgr import GetSlotMgr
from . import define


class CSlotUI(QGraphicsPolygonItem):
    def __init__(self, uid, oSlot, parent=None):
        super(CSlotUI, self).__init__(parent)
        self.m_Uid = uid
        self.m_Slot = weakref.ref(oSlot)
        self.m_PinLine = None
        self.m_PinLineInfo = {}       # 槽的连线列表
        self.InitUI()

    def InitUI(self):
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        self.setFlag(QGraphicsItem.ItemIsSelectable, False)
        self.setZValue(4)
        self.setAcceptHoverEvents(True)

        size = self.m_Slot().GetSize()
        self.m_PF = QRectF(0, 0, size[0], size[1])
        self.setPolygon(QPolygonF(self.m_PF))
        self.setCursor(Qt.CrossCursor)

    def GetIDInfo(self):
        return 1, 1, 1  # TODO

    def GetChartName(self):
        return self.m_Slot().GetChartName()

    def GetSlotType(self):
        return self.m_Slot().GetSlotType()

    def GetVarType(self):
        return self.m_Slot().GetVarType()

    def GetChartID(self):
        return self.m_Slot().GetChartID()

    def IsInputSlotUI(self):
        return self.GetSlotType() == define.INPUT_BTN_TYPE

    def GetConnectPoint(self):
        return self.m_Slot().m_Center

    def mousePressEvent(self, event):
        super(CSlotUI, self).mousePressEvent(event)
        event.accept()
        if event.button() == Qt.LeftButton:
            self.scene().BeginConnect(self)

    def mouseMoveEvent(self, event):
        super(CSlotUI, self).mouseMoveEvent(event)
        event.accept()
        if event.button() == Qt.LeftButton:
            self.update()
            lastuid = GetSlotMgr().GetLastSelect()
            if not lastuid:
                GetSlotMgr().SetLastSelect(self.m_Uid)

    def mouseReleaseEvent(self, event):
        event.accept()
        super(CSlotUI, self).mouseReleaseEvent(event)
        if event.button() == Qt.LeftButton:
            self.scene().EndConnect(event)

    def contextMenuEvent(self, _):
        if not self.GetPinLine() and not self.m_PinLineInfo:
            return
        menu = QMenu()
        if self.IsInputSlotUI():
            func = misc.Functor(self.OnDelConnect, self.m_PinLine)
            menu.addAction("删除连线", func)
        else:
            for _, wPinLine in self.m_PinLineInfo.items():
                sName = wPinLine().GetStartSlotChartName()
                sMsg = "删除与%s的连线" % sName
                func = misc.Functor(self.OnDelConnect, wPinLine)
                menu.addAction(sMsg, func)
        menu.exec_(QCursor.pos())

    def OnDelConnect(self, wPinLine):
        if not wPinLine:
            return
        oPinLine = wPinLine()
        self.scene().DelConnect(oPinLine)

    def CanConnect(self, oSlotUI):
        """判断self是否可以和oSlotUI连接"""
        if self.m_Uid == oSlotUI.m_Uid:  # 槽不能和自己连接
            return False
        if self.GetChartID() == oSlotUI.GetChartID():   # 同一个节点不能连接
            return False
        if self.GetSlotType() == oSlotUI.GetSlotType():  # 同输入或者同输出不能连接
            return False
        if self.GetVarType() != oSlotUI.GetVarType():   # 相同的变量类型才能连接
            return False
        return True

    def Relase(self):
        if self.IsInputSlotUI():
            self.OnDelConnect(self.m_PinLine)
            return
        lst = []
        for _, wPinLine in self.m_PinLineInfo.items():
            lst.append(wPinLine)
        for wPinLine in lst:
            self.OnDelConnect(wPinLine)
        GetSlotMgr().Relase(self.m_Uid)
        self.setParentItem(None)
        self.m_PinLineInfo = {}
        self.m_PinLine = None

    # input
    def SetPinLine(self, oPinLine):
        if not oPinLine:
            self.m_PinLine = None
        else:
            self.m_PinLine = weakref.ref(oPinLine)

    def GetPinLine(self):
        if self.m_PinLine:
            return self.m_PinLine()
        return None

    # output
    def AddPinLine(self, oPinLine):
        if not oPinLine:
            return
        self.m_PinLineInfo[oPinLine.GetUid()] = weakref.ref(oPinLine)

    def DelPinLine(self, oPinLine):
        uid = oPinLine.GetUid()
        if uid in self.m_PinLineInfo:
            del self.m_PinLineInfo[uid]

    def UpdateLinePosition(self):
        if self.IsInputSlotUI():
            line = self.GetPinLine()
            if line:
                line.UpdatePosition()
            return
        for _, wPinLine in self.m_PinLineInfo.items():
            wPinLine().UpdatePosition()


class CPinLine(QGraphicsItem):
    """引脚连线"""

    def __init__(self, lineID=0, parent=None):
        super(CPinLine, self).__init__(parent)
        self.m_LineID = lineID
        self.m_UID = miscqt.NewUuid()
        self.m_StartSlotUI = None
        self.m_EndSlotUI = None
        self.setZValue(-1000)
        self.m_StartPoint = None
        self.m_EndPoint = None
        self.m_Path = None
        self.m_Rect = None
        self.RecalculateShapeAndBount()

    def GetUid(self):
        return self.m_UID

    def GetStartSlotChartName(self):
        oSlotUI = self.GetStartSlotUI()
        sName = oSlotUI.GetChartName()
        return sName

    def RecalculateShapeAndBount(self):
        if self.m_StartPoint is None or self.m_EndPoint is None:
            self.m_Path = QPainterPath()
            self.m_Path.addRect(0, 0, 0, 0)
            self.m_Rect = self.m_Path.boundingRect()
            return
        if self.m_StartPoint.x() < self.m_EndPoint.x():
            centerY = (self.m_StartPoint.y() + self.m_EndPoint.y()) // 2
            c1 = QPointF(self.m_StartPoint.x(), centerY)
            c2 = QPointF(self.m_EndPoint.x(), centerY)
        else:
            centerX = (self.m_StartPoint.x() + self.m_EndPoint.x()) // 2
            c1 = QPointF(centerX, self.m_StartPoint.y())
            c2 = QPointF(centerX, self.m_EndPoint.y())
        self.m_Path = QPainterPath()
        self.m_Path.moveTo(self.m_StartPoint)
        self.m_Path.cubicTo(c1, c2, self.m_EndPoint)
        self.m_Path.addEllipse(self.m_StartPoint, 4, 4)
        self.m_Path.addEllipse(self.m_EndPoint, 4, 4)
        self.m_Rect = self.m_Path.boundingRect()

    def SetStartReceiver(self, oSlotUI):
        self.m_StartSlotUI = weakref.ref(oSlotUI)
        self.UpdatePosition()

    def GetStartSlotUI(self):
        if self.m_StartSlotUI:
            return self.m_StartSlotUI()
        return None

    def SetEndReceiver(self, oSlotUI):
        self.m_EndSlotUI = weakref.ref(oSlotUI)
        self.UpdatePosition()

    def GetEndSlotUI(self):
        if self.m_EndSlotUI:
            return self.m_EndSlotUI()
        return None

    def UpdatePosition(self):
        startSlotUI = self.GetStartSlotUI()
        if startSlotUI:
            self.m_StartPoint = self.mapFromItem(startSlotUI, *startSlotUI.GetConnectPoint())
        endSlotUI = self.GetEndSlotUI()
        if endSlotUI:
            self.m_EndPoint = self.mapFromItem(endSlotUI, *endSlotUI.GetConnectPoint())
        else:
            self.m_EndPoint = self.mapFromScene(self.scene().GetMouseScenePos())
        self.prepareGeometryChange()
        self.RecalculateShapeAndBount()

    def paint(self, painter, _, __):
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setPen(Qt.white)
        painter.drawPath(self.m_Path)
