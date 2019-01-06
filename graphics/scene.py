# -*- coding:utf-8 -*-
"""
@Author: xiaohao
@Date: 2018-11-21 14:47:43
@Desc: 蓝图场景
"""


from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtGui import QTransform, QCursor, QPolygonF
from PyQt5.QtCore import QPointF, Qt

from . import nodeui, pinui, lineui
from editdata import interface
from signalmgr import GetSignal
from viewmgr.uimgr import GetUIMgr
from viewmgr.statusmgr import GetStatusMgr
from editdata.idmgr import GetIDMgr


class CBlueprintScene(QGraphicsScene):
    def __init__(self, bpID, parent=None):
        super(CBlueprintScene, self).__init__(parent)
        self.m_BPID = bpID
        self.m_PinInfo = {}
        self.m_TempPinLine = None   # 临时引脚连线
        self.m_IsNodeMove = False   # 节点是否有移动
        self.m_StartPos = None      # 节点移动的起始坐标
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

    def GetBPID(self):
        return self.m_BPID

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
                GetStatusMgr().ClearNode(self.m_BPID)

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
            selectNode = GetStatusMgr().GetSelectNode(self.m_BPID)
            if nodeID not in selectNode:
                GetStatusMgr().SelectOneNode(self.m_BPID, nodeID)
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
                GetStatusMgr().ChangeSelectNode(self.m_BPID, nodeID)
            else:
                GetStatusMgr().SelectOneNode(self.m_BPID, nodeID)

    def keyPressEvent(self, event):
        super(CBlueprintScene, self).keyPressEvent(event)
        if event.key() == Qt.Key_Delete:
            lstNode = GetStatusMgr().GetSelectNode(self.m_BPID)
            for nodeID in lstNode:
                self.OnDelNodeUI(nodeID)

    def wheelEvent(self, event):
        super(CBlueprintScene, self).wheelEvent(event)
        # 吞噬信号，不再将信号返回父窗口，禁止父窗口滑动条操作
        event.accept()

    def RubberBandSelecNodeUI(self, path, mode, trans):
        selectItems = self.items(path, mode, Qt.DescendingOrder, trans)
        allItems = self.items()
        selectNode = GetStatusMgr().GetSelectNode(self.m_BPID)
        for item in allItems:
            if not isinstance(item, nodeui.CNodeUI):
                continue
            nodeID = item.m_NodeID
            if item in selectItems:
                if nodeID not in selectNode:
                    GetStatusMgr().ChangeSelectNode(self.m_BPID, nodeID)
            elif nodeID in selectNode:
                GetStatusMgr().DelSelectNode(self.m_BPID, nodeID)

    # ----------------------node-------------------------------------
    def SetNodeMove(self, offpos):
        for nodeID in GetStatusMgr().GetSelectNode(self.m_BPID):
            oNodeUI = GetUIMgr().GetNodeUI(nodeID)
            oNodeUI.SetMouseMovePos(offpos)

    def AddNodeUI(self, nodeID, tPos):
        oNodeUI = nodeui.CNodeUI(nodeID)
        self.addItem(oNodeUI)
        x, y = tPos
        oNodeUI.setPos(x, y)

    def OnDelNodeUI(self, nodeID):
        interface.DelNode(nodeID)
        self._DelNodeUI(nodeID)

    def _DelNodeUI(self, nodeID):
        oNodeUI = GetUIMgr().GetNodeUI(nodeID)
        GetStatusMgr().DelSelectNode(self.m_BPID, nodeID)
        if not oNodeUI:
            return
        self.removeItem(oNodeUI)

    def BeginConnect(self, startPinID):
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
                self._AddLineUI(inputPinID, outputPinID)

        self.removeItem(self.m_TempPinLine)
        self.m_TempPinLine = None

    def _AddLineUI(self, inputPinID, outputPinID):
        """真正执行添加连接线"""
        lineID = interface.AddLine(self.m_BPID, outputPinID, inputPinID)
        line = lineui.CLineUI(lineID)
        self.addItem(line)
        line.SetStartPinID(outputPinID)
        line.SetEndPinID(inputPinID)

    def OnDelLineUI(self, lineID):
        interface.DelLine(lineID)
        self._DelLineUI(lineID)

    def S_OnDelLineUI(self, lineID):
        bpID = GetIDMgr().GetBPByLine(lineID)
        if bpID == self.m_BPID:
            self._DelLineUI(lineID)

    def _DelLineUI(self, lineID):
        oLineUI = GetUIMgr().GetLineUI(lineID)
        self.removeItem(oLineUI)

    def GetMouseScenePos(self):
        view = self.views()[0]
        viewPos = view.mapFromGlobal(QCursor.pos())
        scenePos = view.mapToScene(viewPos)
        return scenePos
