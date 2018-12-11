# -*- coding:utf-8 -*-
"""
@Author: xiaohao
@Date: 2018-11-21 14:48:22
@Desc: 节点ui
"""


from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QGraphicsProxyWidget, QGraphicsItem, QPushButton, QWidget
from PyQt5.QtCore import Qt

from . import uimgr, pinui
from editdata import interface

import editdata.define as eddefine
import bpdata.define as bddefine


class CNodeUI(QGraphicsProxyWidget):
    def __init__(self, bpID, nodeID, parent=None):
        super(CNodeUI, self).__init__(parent)
        self.m_BPID = bpID
        self.m_NodeID = nodeID
        self.m_StartPos = None
        self.m_NodeWidget = CNodeWidget(bpID, nodeID)
        self.InitUI()
        self.InitSlot()
        uimgr.GetUIMgr().AddNodeUI(bpID, nodeID, self)

    def InitUI(self):
        self.setWidget(self.m_NodeWidget)
        self.setAcceptHoverEvents(True)
        self.setAcceptedMouseButtons(Qt.LeftButton)
        self.setFlags(
            QGraphicsItem.ItemIsSelectable |
            QGraphicsItem.ItemIsMovable |
            QGraphicsItem.ItemSendsGeometryChanges
        )
        self.setZValue(4)

    def InitSlot(self):
        """四个槽的初始化,先手动设置"""
        iOffset = 10
        for pinID, oBtn in self.m_NodeWidget.m_ButtonInfo.items():
            if oBtn.IsOutput():
                center = (oBtn.width() + iOffset, oBtn.height() / 2)
            else:
                center = (0 - iOffset, oBtn.height() / 2)
            oPinUI = pinui.CPinUI(self.m_BPID, self.m_NodeID, pinID)
            oPinUI.SetCenter(center)
            oPinUI.SetPolygon(oBtn.width(), oBtn.height())
            oPinUI.setParentItem(self)
            x, y = self.pos().x(), self.pos().y()
            x += oBtn.x()
            y += oBtn.y()
            mfsPos = oPinUI.mapFromScene(x, y)
            mtpPos = oPinUI.mapToParent(mfsPos)
            oPinUI.setPos(mtpPos.x(), mtpPos.y())

    def IsDrawLine(self):
        return self.scene().m_IsDrawLine

    def contextMenuEvent(self, event):
        event.accept()
        menu = QtWidgets.QMenu()
        menu.addAction("删除节点", self.S_OnDelNodeUI)
        menu.exec_(QtGui.QCursor.pos())

    def mousePressEvent(self, event):
        super(CNodeUI, self).mousePressEvent(event)
        event.accept()
        if self.IsDrawLine():
            return
        if event.button() == Qt.LeftButton:
            self.m_StartPos = event.pos()

    def mouseMoveEvent(self, event):
        super(CNodeUI, self).mouseMoveEvent(event)
        if self.IsDrawLine():
            return
        self.SetMouseMovePos(self.m_StartPos, event.pos())

    def mouseReleaseEvent(self, event):
        super(CNodeUI, self).mouseReleaseEvent(event)
        self.m_StartPos = None
        self.setSelected(True)

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionHasChanged:
            for lineID in interface.GetAllLineByNode(self.m_BPID, self.m_NodeID):
                oLineUI = uimgr.GetUIMgr().GetLineUI(self.m_BPID, lineID)
                oLineUI.UpdatePosition()
        return super(CNodeUI, self).itemChange(change, value)

    def SetMouseMovePos(self, sPos, ePos):
        if not (sPos and ePos):
            return
        pos = self.pos()
        x = pos.x() + ePos.x() - sPos.x()
        y = pos.y() + ePos.y() - sPos.y()
        self.setPos(x, y)

    def S_OnDelNodeUI(self):
        interface.DelNode(self.m_BPID, self.m_NodeID)
        self.m_NodeWidget = None
        self.scene().DelNodeUI(self.m_NodeID)


QSS_STYLE = """
QWidget#CNodeWidget{
    background:transparent;
}
QWidget#BCWidget{
    background:rgba(0, 0, 0, 200);
    border-style:solid;
    border-width:0px;
    border-radius:10px;
}
QWidget#top{
    border-style:solid;
    border-width:0px;
    background:qlineargradient(spread:pad, x1:0.00564972, y1:0.358, x2:1, y2:0.637, stop:0 rgba(0, 104, 183, 200), stop:1 rgba(0, 160, 233, 50));
    border-top-left-radius:10px;
    border-top-right-radius:10px;
    border-bottom-left-radius:0px;
    border-bottom-right-radius:0px;
}
QLabel{
    color:white;
}
QPushButton{
    background-color:transparent;
    color:white;
    border:none;
}
QPushButton:hover{
    background:qlineargradient(spread:pad, x1:0, y1:1, x2:1, y2:1, stop:0 rgba(255, 0, 0, 0), stop:0.175141 rgba(255, 255, 255, 100), stop:0.824859 rgba(255, 255, 255, 100), stop:1 rgba(0, 0, 255, 0));
    border-image:transparent;
    color:white;
}
QWidget#outline{
    background:transparent;
    border:4px solid rgb(244, 100, 0);
    border-radius:14px;
}
"""


class CNodeWidget(QWidget):
    def __init__(self, bpID, nodeID, parent=None):
        super(CNodeWidget, self).__init__(parent)
        self.m_BPID = bpID
        self.m_NodeID = nodeID

        self.m_NodeName = interface.GetNodeAttr(bpID, nodeID, eddefine.NodeAttrName.NAME)
        self.m_PinInfo = interface.GetNodeAttr(bpID, nodeID, eddefine.NodeAttrName.PININFO)
        self.m_InputInfo = []
        self.m_OutputInfo = []
        self.m_ButtonInfo = {}
        self.InitData()
        self.InitUI()

    def InitData(self):
        for pid, pinInfo in self.m_PinInfo.items():
            iPinType = pinInfo[bddefine.PinAttrName.PIN_TYPE]
            if iPinType == bddefine.PIN_INPUT_TYPE:
                tmp = self.m_InputInfo
            else:
                tmp = self.m_OutputInfo
            if bddefine.PinAttrName.DATA_TYPE in pinInfo:
                tmp.append([self.m_BPID, self.m_NodeID, pid])
            else:
                tmp.insert(0, [self.m_BPID, self.m_NodeID, pid])

    def AddButton(self, oBtn):
        if not oBtn:
            return
        self.m_ButtonInfo[oBtn.GetPinID()] = oBtn

    def InitUI(self):
        self.setObjectName("CNodeWidget")
        self.setStyleSheet(QSS_STYLE)
        self.setCursor(Qt.SizeAllCursor)
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.BCWidget = QtWidgets.QWidget(self)
        self.BCWidget.setObjectName("BCWidget")
        self.verticalLayout_BCWidget = QtWidgets.QVBoxLayout(self.BCWidget)
        self.verticalLayout_BCWidget.setObjectName("verticalLayout_BCWidget")

        # top
        self.top = QtWidgets.QWidget(self.BCWidget)
        self.top.setObjectName("top")
        self.horizontalLayout_top = QtWidgets.QHBoxLayout(self.top)
        self.horizontalLayout_top.setContentsMargins(6, 2, 4, 2)
        self.horizontalLayout_top.setObjectName("horizontalLayout_top")
        self.lb_Title = QtWidgets.QLabel(self.top)
        self.lb_Title.setObjectName("lb_Title")
        self.lb_Title.setText(self.m_NodeName)
        self.horizontalLayout_top.addWidget(self.lb_Title)
        spacerItem = QtWidgets.QSpacerItem(67, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_top.addItem(spacerItem)
        self.verticalLayout_BCWidget.addWidget(self.top)

        # for attr
        maxLen = max(len(self.m_InputInfo), len(self.m_OutputInfo))
        for i in range(maxLen):
            qHL = QtWidgets.QHBoxLayout()
            oInBtn = oOutBtn = None
            if i < len(self.m_InputInfo) and self.m_InputInfo[i]:
                oInBtn = CNodeButtonUI(*self.m_InputInfo[i], False, self.BCWidget)
            if i < len(self.m_OutputInfo) and self.m_OutputInfo[i]:
                oOutBtn = CNodeButtonUI(*self.m_OutputInfo[i], True, self.BCWidget)
            spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
            if oInBtn:
                qHL.addWidget(oInBtn)
                self.AddButton(oInBtn)
            qHL.addItem(spacerItem)
            if oOutBtn:
                qHL.addWidget(oOutBtn)
                self.AddButton(oOutBtn)
            self.verticalLayout_BCWidget.addLayout(qHL)

        self.verticalLayout.addWidget(self.BCWidget)


class CNodeButtonUI(QPushButton):
    def __init__(self, bpID, nodeID, pinID, bOutput=False, parent=None):
        super(CNodeButtonUI, self).__init__(parent)
        self.m_BPID = bpID
        self.m_NodeID = nodeID
        self.m_PinID = pinID
        self.m_BOutPut = bOutput
        self.setCursor(Qt.PointingHandCursor)
        if bOutput:
            self.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.SetIcon()
        self.SetText()
        uimgr.GetUIMgr().AddPinBtnUI(bpID, nodeID, pinID, self)

    def GetPinID(self):
        return self.m_PinID

    def IsOutput(self):
        return self.m_BOutPut

    def GetPinInfo(self):
        dNodeInfo = interface.GetNodeAttr(self.m_BPID, self.m_NodeID, eddefine.NodeAttrName.PININFO)
        return dNodeInfo[self.m_PinID]

    def SetIcon(self, iType=None):
        if iType is None:
            pinInfo = self.GetPinInfo()
            iType = pinInfo.get(bddefine.PinAttrName.DATA_TYPE, -1)
        icon = QtGui.QIcon()
        pix = ":/icon/btn_%s.png" % iType
        icon.addPixmap(QtGui.QPixmap(pix), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setIcon(icon)
        self.setIconSize(QtCore.QSize(20, 20))

    def SetText(self, sText=None):
        if sText is None:
            pinInfo = self.GetPinInfo()
            sText = pinInfo[bddefine.PinAttrName.NAME]
        self.setText(sText)
