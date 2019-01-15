# -*- coding:utf-8 -*-
"""
@Author: xiaohao
@Date: 2018-11-21 14:48:22
@Desc: 节点ui
"""


from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QGraphicsProxyWidget, QGraphicsItem, QPushButton, QWidget
from PyQt5.QtCore import Qt, QPoint

from . import pinui
from editdata import interface
from viewmgr.uimgr import GetUIMgr
from pubcode import functor
import bpdata.define as bddefine


QSS_NODE_UNPRESS = """
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
"""

QSS_NODE_PRESS = QSS_NODE_UNPRESS + """
QWidget#outline{
    background:transparent;
    border:4px solid rgb(241, 176, 0);
    border-radius:14px;
}
"""


class CNodeUI(QGraphicsProxyWidget):
    m_OutlineBorder = 4

    def __init__(self, nodeID, parent=None):
        super(CNodeUI, self).__init__(parent)
        self.m_NodeID = nodeID
        self.m_StartPos = None
        self.m_IsNodeMove = False   # 是否节点有拖动
        self.m_NodeWidget = CNodeWidget(nodeID)
        self.InitUI()
        GetUIMgr().AddNodeUI(nodeID, self)

    def __del__(self):
        GetUIMgr().DelNodeUI(self.m_NodeID)

    def InitUI(self):
        self.setWidget(self.m_NodeWidget)
        self.setAcceptHoverEvents(True)
        self.setAcceptedMouseButtons(Qt.LeftButton)
        self.setFlags(
            QGraphicsItem.ItemIsSelectable |
            QGraphicsItem.ItemIsMovable |
            QGraphicsItem.ItemSendsGeometryChanges |
            QGraphicsItem.ItemIsFocusable
        )
        self.setZValue(4)
        self.SetUnpressStyle()

    def GetID(self):
        return self.m_NodeID

    def ToScenePos(self, gPos):
        return self.scene().GetMouseScenePos(gPos)

    def contextMenuEvent(self, event):
        event.accept()
        menu = QtWidgets.QMenu()
        menu.addAction("删除节点", self.S_OnDelNodeUI)
        menu.exec_(QtGui.QCursor.pos())

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionHasChanged:
            for lineID in interface.GetAllLineByNode(self.m_NodeID):
                oLineUI = GetUIMgr().GetLineUI(lineID)
                if oLineUI:
                    oLineUI.UpdatePosition()
        return super(CNodeUI, self).itemChange(change, value)

    def SetMouseMovePos(self, offpos):
        pos = self.pos() + offpos
        self.setPos(pos)
        self.m_IsNodeMove = True
        interface.SetNodeAttr(self.m_NodeID, bddefine.NodeAttrName.POSITION, (pos.x(), pos.y()))

    def S_OnDelNodeUI(self):
        self.scene().OnDelNodeUI(self.m_NodeID)

    def SetPressStyle(self):
        self.m_NodeWidget.setStyleSheet(QSS_NODE_PRESS)
        self.setZValue(self.zValue() + 2)

    def SetUnpressStyle(self):
        self.m_NodeWidget.setStyleSheet(QSS_NODE_UNPRESS)
        self.setZValue(self.zValue() - 2)

    # def mousePressEvent(self, event):
    #     super(CNodeUI, self).mousePressEvent(event)
    #     ePos = event.pos()
    #     print("node-pos", ePos)
    #     print("node-scenepos", self.mapToScene(ePos))
    #     print("-"*20)


class CNodeWidget(QWidget):
    def __init__(self, nodeID, parent=None):
        super(CNodeWidget, self).__init__(parent)
        self.m_NodeID = nodeID
        self.m_NodeDisplayName = interface.GetNodeAttr(nodeID, bddefine.NodeAttrName.DISPLAYNAME)
        self.InitUI()

    def _PinIsInput(self, pinID):
        iPinType = interface.GetPinAttr(pinID, bddefine.PinAttrName.PIN_TYPE)
        return bddefine.PinIsInput(iPinType)

    def InitUI(self):
        self.setObjectName("CNodeWidget")
        self.setCursor(Qt.SizeAllCursor)
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.outline = QtWidgets.QWidget(self)
        self.outline.setObjectName("outline")
        self.verticalLayout_outline = QtWidgets.QVBoxLayout(self.outline)
        self.verticalLayout_outline.setContentsMargins(4, 4, 4, 4)
        self.verticalLayout_outline.setObjectName("verticalLayout_outline")

        self.BCWidget = QtWidgets.QWidget(self.outline)
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
        self.lb_Title.setText(self.m_NodeDisplayName)
        self.horizontalLayout_top.addWidget(self.lb_Title)
        spacerItem = QtWidgets.QSpacerItem(67, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_top.addItem(spacerItem)

        # add调试label图标
        self.lable_debug = QtWidgets.QLabel(self.top)
        self.lable_debug.setMinimumSize(QtCore.QSize(20, 20))
        self.lable_debug.setMaximumSize(QtCore.QSize(20, 20))
        self.lable_debug.setPixmap(QtGui.QPixmap(":/icon/debug.png"))
        self.lable_debug.setScaledContents(True)
        self.lable_debug.hide()

        self.horizontalLayout_top.addWidget(self.lable_debug)
        self.verticalLayout_BCWidget.addWidget(self.top)

        # fot attr
        hBox = QtWidgets.QHBoxLayout()
        self.m_InputVBox = QtWidgets.QVBoxLayout()
        self.m_OutputVBox = QtWidgets.QVBoxLayout()
        lstPin = interface.GetNodeAttr(self.m_NodeID, bddefine.NodeAttrName.PINIDLIST)
        for pinID in lstPin:
            self._AddPinWidget(pinID)

        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        hBox.addLayout(self.m_InputVBox)
        hBox.addItem(spacerItem)
        hBox.addLayout(self.m_OutputVBox)

        self.verticalLayout_BCWidget.addLayout(hBox)
        self.verticalLayout_outline.addWidget(self.BCWidget)
        self.verticalLayout.addWidget(self.outline)

    def _AddPinWidget(self, pinID):
        if self._PinIsInput(pinID):
            vBox = self.m_InputVBox
            dirc = Qt.LeftToRight
        else:
            vBox = self.m_OutputVBox
            dirc = Qt.RightToLeft

        pinWidget = pinui.CPinUI(pinID, self)
        pinWidget.setLayoutDirection(dirc)
        vBox.addWidget(pinWidget)
        vBox.setAlignment(pinWidget, Qt.AlignLeft)
