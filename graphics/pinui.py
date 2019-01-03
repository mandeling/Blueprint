# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-12-10 17:42:21
@Desc: 引脚ui
"""


import bpdata.define as bddefine

from PyQt5 import QtWidgets, QtCore, QtGui
from pubcode import functor
from editdata import interface
from viewmgr.uimgr import GetUIMgr


class CPinUI(QtWidgets.QGraphicsPolygonItem):
    """节点的槽UI"""

    def __init__(self, pinID, parent=None):
        super(CPinUI, self).__init__(parent)
        # 位置需要优化下
        self.m_PinID = pinID
        self.m_Center = None
        self.InitUI()
        GetUIMgr().AddPinUI(pinID, self)

    def __del__(self):
        GetUIMgr().DelPinUI(self.m_PinID)

    def GetPID(self):
        return self.m_PinID

    def SetCenter(self, center):
        """设置连线中心，相对于父类"""
        self.m_Center = center

    def GetCenter(self):
        return self.m_Center

    def SetPolygon(self, width, heigh):
        """设置polygon"""
        rectF = QtCore.QRectF(0, 0, width, heigh)
        self.setPolygon(QtGui.QPolygonF(rectF))

    def InitUI(self):
        self.setFlag(QtWidgets.QGraphicsItem.ItemSendsGeometryChanges)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, False)
        self.setZValue(2)
        self.setAcceptHoverEvents(True)
        self.setCursor(QtCore.Qt.CrossCursor)

    def mousePressEvent(self, event):
        super(CPinUI, self).mousePressEvent(event)
        event.accept()
        if event.button() == QtCore.Qt.LeftButton:
            self.scene().BeginConnect(self.m_PinID)

    def mouseMoveEvent(self, event):
        super(CPinUI, self).mouseMoveEvent(event)
        event.accept()
        if event.button() == QtCore.Qt.LeftButton:
            self.update()

    def mouseReleaseEvent(self, event):
        event.accept()
        super(CPinUI, self).mouseReleaseEvent(event)
        if event.button() == QtCore.Qt.LeftButton:
            self.scene().EndConnect(event)

    def contextMenuEvent(self, _):
        lstLineID = interface.GetAllLineByPin(self.m_PinID)
        if not lstLineID:
            return
        menu = QtWidgets.QMenu()
        for lineID in lstLineID:
            oPinID = interface.GetLineOtherPin(lineID, self.m_PinID)
            sPinDisplayName = interface.GetPinAttr(oPinID, bddefine.PinAttrName.DISPLAYNAME)
            nodeID = interface.GetNodeIDByPinID(oPinID)
            sNodeDisplayName = interface.GetNodeAttr(nodeID, bddefine.NodeAttrName.DISPLAYNAME)
            sMsg = "删除与%s节点%s引脚的连线" % (sNodeDisplayName, sPinDisplayName)
            func = functor.Functor(self.OnDelConnect, lineID)
            menu.addAction(sMsg, func)
        menu.exec_(QtGui.QCursor.pos())

    def OnDelConnect(self, lineID):
        self.scene().DelConnect(lineID)
