# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-12-10 17:42:21
@Desc: 引脚ui
"""

import misc

from . import myinterface
from PyQt5 import QtWidgets, QtCore, QtGui


class CPinUI(QtWidgets.QGraphicsPolygonItem):
    def __init__(self, bpID, nodeID, pinID, parent=None):
        super(CPinUI, self).__init__(parent)
        self.m_BPID = bpID
        self.m_NodeID = nodeID
        self.m_PinID = pinID
        self.m_Center = None
        self.m_IsInput = myinterface.IsInputPin(bpID, nodeID, pinID)
        self.InitUI()

    def SetCenter(self, center):
        """设置连线中心，相对于父类"""
        self.m_Center = center

    def SetPolygon(self, width, heigh):
        """设置polygon"""
        rectF = QtCore.QRectF(0, 0, width, heigh)
        self.setPolygon(QtGui.QPolygonF(rectF))

    def InitUI(self):
        self.setFlag(QtWidgets.QGraphicsItem.ItemSendsGeometryChanges)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, False)
        self.setZValue(4)
        self.setAcceptHoverEvents(True)
        self.setCursor(QtCore.Qt.CrossCursor)

    def GetIDInfo(self):
        return self.m_BPID, self.m_NodeID, self.m_PinID

    def mousePressEvent(self, event):
        super(CPinUI, self).mousePressEvent(event)
        event.accept()
        if event.button() == QtCore.Qt.LeftButton:
            self.scene().BeginConnect(self)

    def mouseMoveEvent(self, event):
        super(CPinUI, self).mouseMoveEvent(event)
        event.accept()
        if event.button() == QtCore.Qt.LeftButton:
            self.update()
            self.scene().SetSelectPin(self.m_NodeID, self.m_PinID)

    def mouseReleaseEvent(self, event):
        event.accept()
        super(CPinUI, self).mouseReleaseEvent(event)
        if event.button() == QtCore.Qt.LeftButton:
            self.scene().EndConnect(event)

    def contextMenuEvent(self, _):
        if not self.GetPinLine() and not self.m_PinLineInfo:
            return
        menu = QtWidgets.QMenu()
        if self.m_IsInput:
            func = misc.Functor(self.OnDelConnect, self.m_PinLine)
            menu.addAction("删除连线", func)
        else:
            for _, wPinLine in self.m_PinLineInfo.items():
                sName = wPinLine().GetStartSlotChartName()
                sMsg = "删除与%s的连线" % sName
                func = misc.Functor(self.OnDelConnect, wPinLine)
                menu.addAction(sMsg, func)
        menu.exec_(QtGui.QCursor.pos())

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
