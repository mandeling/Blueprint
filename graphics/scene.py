# -*- coding:utf-8 -*-
"""
@Author: xiaohao
@Date: 2018-11-21 14:47:43
@Desc: 蓝图场景
"""

import weakref
import time

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtGui import QTransform, QCursor, QPolygonF
from PyQt5.QtCore import QPointF, Qt

from . import nodeui, pinui, lineui
from editdata import interface
from signalmgr import GetSignal
from viewmgr.uimgr import GetUIMgr
from viewmgr.statusmgr import GetStatusMgr
import bpdata.define as bddefine


class CBlueprintScene(QGraphicsScene):
    def __init__(self, graphicID, parent=None):
        super(CBlueprintScene, self).__init__(parent)
        self.m_GraphicID = graphicID
        self.m_PinInfo = {}
        self.m_TempPinLine = None   # 临时引脚连线
        self.m_IsNodeMove = False   # 节点是否有移动
        self.m_StartPos = None      # 节点移动的起始坐标
        self.m_ReleaseTime = 0      # 连线记录释放时间
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
        GetSignal().DEL_LINE.connect(self.S_OnDelLineUI)
        GetSignal().DEL_NODE.connect(self.S_OnDelNodeUI)
        GetSignal().NEW_NODE.connect(self.S_OnNewNodeUI)

        GetSignal().UI_LINE_PRESS.connect(self.S_LineOnPress)
        GetSignal().UI_LINE_MOVE.connect(self.S_LineOnMove)
        GetSignal().UI_LINE_RELEASE.connect(self.S_LineOnRelease)
        GetSignal().UI_LINE_CONNECT.connect(self.S_LineOnConnect)

    def GetGraphicID(self):
        return self.m_GraphicID

    def GetMouseScenePos(self, gPos):
        view = self.views()[0]
        viewPos = view.mapFromGlobal(gPos)
        scenePos = view.mapToScene(viewPos)
        return scenePos

    # ----------------------各种事件-------------------------------------
    def mousePressEvent(self, event):
        super(CBlueprintScene, self).mousePressEvent(event)
        if self.m_TempPinLine:
            return
        self.M_NodeMousePressEvent(event)

    def M_NodeMousePressEvent(self, event):
        item = self.itemAt(event.scenePos(), QTransform())
        if event.button() == Qt.LeftButton:
            if item and isinstance(item, nodeui.CNodeUI):
                self.m_StartPos = event.scenePos()
            else:
                GetStatusMgr().ClearNode(self.m_GraphicID)

    def mouseMoveEvent(self, event):
        super(CBlueprintScene, self).mouseMoveEvent(event)
        if self.m_TempPinLine:
            self.m_TempPinLine.UpdatePosition()
            return
        self.M_NodeMouseMoveEvent(event)

    def M_NodeMouseMoveEvent(self, event):
        item = self.itemAt(event.scenePos(), QTransform())
        if not (item and isinstance(item, nodeui.CNodeUI)):
            return
        if self.m_StartPos:
            nodeID = item.GetID()
            selectNode = GetStatusMgr().GetSelectNode(self.m_GraphicID)
            if nodeID not in selectNode:
                GetStatusMgr().SelectOneNode(self.m_GraphicID, nodeID)
            self.SetNodeMove(event.scenePos() - self.m_StartPos)
            self.m_StartPos = event.scenePos()
            self.m_IsNodeMove = True

    def mouseReleaseEvent(self, event):
        super(CBlueprintScene, self).mouseReleaseEvent(event)
        self.M_NodeMouseReleaseEvent(event)

    def M_NodeMouseReleaseEvent(self, event):
        self.m_StartPos = None
        if self.m_IsNodeMove:
            self.m_IsNodeMove = False
            return
        item = self.itemAt(event.scenePos(), QTransform())
        if not (item and isinstance(item, nodeui.CNodeUI)):
            return
        if event.button() == Qt.LeftButton:
            nodeID = item.GetID()
            if event.modifiers() == Qt.ControlModifier:
                GetStatusMgr().ChangeSelectNode(self.m_GraphicID, nodeID)
            else:
                GetStatusMgr().SelectOneNode(self.m_GraphicID, nodeID)

    def keyPressEvent(self, event):
        super(CBlueprintScene, self).keyPressEvent(event)
        if event.key() == Qt.Key_Delete:
            lstNode = GetStatusMgr().GetSelectNode(self.m_GraphicID)
            for nodeID in lstNode:
                self.OnDelNodeUI(nodeID)

    def wheelEvent(self, event):
        super(CBlueprintScene, self).wheelEvent(event)
        # 吞噬信号，不再将信号返回父窗口，禁止父窗口滑动条操作
        event.accept()

    def RubberBandSelecNodeUI(self, path, mode, trans):
        selectItems = self.items(path, mode, Qt.DescendingOrder, trans)
        allItems = self.items()
        selectNode = GetStatusMgr().GetSelectNode(self.m_GraphicID)
        for item in allItems:
            if not isinstance(item, nodeui.CNodeUI):
                continue
            nodeID = item.m_NodeID
            if item in selectItems:
                if nodeID not in selectNode:
                    GetStatusMgr().ChangeSelectNode(self.m_GraphicID, nodeID)
            elif nodeID in selectNode:
                GetStatusMgr().DelSelectNode(self.m_GraphicID, nodeID)

    # ----------------------node-------------------------------------
    def SetNodeMove(self, offpos):
        for nodeID in GetStatusMgr().GetSelectNode(self.m_GraphicID):
            oNodeUI = GetUIMgr().GetNodeUI(nodeID)
            oNodeUI.SetMouseMovePos(offpos)

    def S_OnNewNodeUI(self, graphicID, nodeID):
        if self.m_GraphicID != graphicID:
            return
        self._NewNodeUI(nodeID)

    def _NewNodeUI(self, nodeID):
        tPos = interface.GetNodeAttr(nodeID, bddefine.NodeAttrName.POSITION)
        oNodeUI = nodeui.CNodeUI(nodeID)
        self.addItem(oNodeUI)
        x, y = tPos
        oNodeUI.setPos(x, y)

    def OnDelNodeUI(self, nodeID):
        interface.DelNode(nodeID)

    def S_OnDelNodeUI(self, graphicID, nodeID):
        if graphicID == self.m_GraphicID:
            self._DelNodeUI(nodeID)

    def _DelNodeUI(self, nodeID):
        GetStatusMgr().DelSelectNode(self.m_GraphicID, nodeID)
        oNodeUI = GetUIMgr().GetNodeUI(nodeID)
        if oNodeUI:
            self.removeItem(oNodeUI)

    # ----------------------line-------------------------------------
    def S_LineOnPress(self, graphicID, startPin):
        if self.m_GraphicID != graphicID:
            return
        self.m_TempPinLine = lineui.CLineUI()
        self.addItem(self.m_TempPinLine)
        self.m_TempPinLine.SetStartPinID(startPin)

    def S_LineOnMove(self, graphicID):
        if self.m_GraphicID != graphicID:
            return
        if self.m_TempPinLine:
            self.m_TempPinLine.UpdatePosition()

    def S_LineOnRelease(self, graphicID):
        if self.m_GraphicID != graphicID:
            return
        self.m_ReleaseTime = time.time()
        self.removeItem(self.m_TempPinLine)

    def S_LineOnConnect(self, graphicID, ePinID):
        if self.m_GraphicID != graphicID:
            return
        if not self.m_TempPinLine:
            return
        if time.time() - self.m_ReleaseTime < 0.2:
            sPinID = self.m_TempPinLine.GetStartPinID()
            if interface.PinCanConnect(sPinID, ePinID):
                if interface.IsInputPin(sPinID):
                    inputPinID, outputPinID = sPinID, ePinID
                else:
                    inputPinID, outputPinID = ePinID, sPinID
                lineID = interface.AddLine(self.m_GraphicID, outputPinID, inputPinID)
                self.AddLineUI(lineID, inputPinID, outputPinID)
        self.m_TempPinLine = None

    def AddLineUI(self, lineID, iPin, oPin):
        """真正执行添加连接线"""
        line = lineui.CLineUI(lineID)
        self.addItem(line)
        line.SetStartPinID(oPin)
        line.SetEndPinID(iPin)

    def S_OnDelLineUI(self, graphicID, lineID):
        if graphicID == self.m_GraphicID:
            oLineUI = GetUIMgr().GetLineUI(lineID)
            if oLineUI:
                self.removeItem(oLineUI)
